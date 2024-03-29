from time import sleep
from Exposure.constants import *
from GUI.constants import *


class SmartExposure:
    from GUI.GUI import GUI

    def __init__(self, app: GUI) -> None:
        self.app = app
        pass

    def _start_smart_NO_exposure(self) -> int:
        total = 0
        try:
            total += self.app.watcher.wait_calib_end()
            self.app.com.end()
        except RuntimeError:
            return total
        return total

    def start_timer(self) -> int:
        total = 5
        for i in range(total, -1, -1):
            sleep(1)
            self.app.messenger.timerMessage(i)
            if self.app.app_state == "stop":
                raise RuntimeError
        return total

    def start_ma_exposure(self) -> int:
        total = 0
        try:
            self.app.statusBox.status_gen_label.configure(text="Gen: Countdown")  # type: ignore
            total = self.start_timer()
            total += self.app.watcher.wait_standby()
            self.app.statusBox.status_gen_label.configure(text="Gen: Standby")  # type: ignore
            self.app.com.start_long()
            total += self.app.watcher.wait_ma_exposure_start()
            self.app.statusBox.status_gen_label.configure(text="Gen: Under exposure")  # type: ignore
            total += self.app.watcher.wait_ma_exposure_end()
            self.app.statusBox.status_gen_label.configure(text="Gen: Blocked")  # type: ignore
            self.app.com.end()

        except RuntimeError:
            self.app.statusBox.status_gen_label.configure(text="Gen: Blocked")  # type: ignore
            return total
        self.app.messenger.exposureMessage(total)
        self.app.control.action("stop")
        return total

    def start_smart_exposure(self) -> int:
        total = 0
        try:
            total += self.app.watcher.wait_standby()
            self.app.statusBox.status_mu_label.configure(text="MU: Standby")  # type: ignore
            self.app.com.start_short()
            self.app.statusBox.status_mu_label.configure(text="MU: Under exposure")  # type: ignore
            total += self.app.watcher.wait_exposure_end()
            self.app.statusBox.status_mu_label.configure(text="MU: Blocked")  # type: ignore
            self.app.com.end()
        except RuntimeError:
            self.app.statusBox.status_mu_label.configure(text="MU: Blocked")  # type: ignore
            return total
        self.app.messenger.exposureMessage(total)
        self.app.control.action("stop")
        return total

    def start_smart_loop(self) -> int:
        total = 0
        exposures = 0
        self.app.set_state_mcu("calibrating")
        self.app.statusBox.status_mcu_label.configure(text="MCU: calibrating")  # type: ignore
        while True:
            try:
                if self.app.app_state == "stop":
                    raise RuntimeError

                total += self.app.watcher.wait_standby(watchPass=True, count=exposures)
                self.app.statusBox.status_mu_label.configure(text="MU: Standby")  # type: ignore

                if self.app.watcher.is_calib_passed():
                    self.app.window_log("Calib Passed!")
                    self.app.statusBox.status_mu_label.configure(text="MU: Calib Pass")  # type: ignore
                    break

                self.app.com.start_short()
                total += self.app.watcher.wait_exposure_start()
                self.app.statusBox.status_mu_label.configure(text="MU: Under exposure")  # type: ignore

                total += self.app.watcher.wait_exposure_end()
                self.app.statusBox.status_mu_label.configure(text="MU: Blocked")  # type: ignore
                exposures += 1
                self.app.com.end()

                if self.app.watcher.is_calib_passed():
                    self.app.window_log("Calib Passed!")
                    self.app.statusBox.status_mu_label.configure(text="MU: Calib Pass")  # type: ignore
                    break

            except RuntimeError:
                self.app.statusBox.status_mu_label.configure(text="MU: Blocked")  # type: ignore
                self.app.control.action("stop")
                break

        if self.app.app_state != "stop":
            self.app.messenger.setExposureMessage(total, exposures)
            if self.app.mode != "auto":
                self.app.control.action("stop")
                return -1

        return total

    def start_auto_loop(self) -> None:
        total = 0
        try:
            for calibration in self.app.selected_cal:

                text = f"Init: {calibration} calib"
                sleep(1)
                total += 1

                self.app.window_log(text)
                self.app.file_log("control", "info", text)
                self.app.current_calib = calibration
                self.app.change_current_calib(calibration)

                text = f"FPD stabilization:"
                self.app.window_log(text)
                for i in range(5):  # type: ignore
                    if self.app.app_state == "stop":
                        raise ConnectionAbortedError
                    sleep(0.5)
                    text = f"FPD stabilization:{'.'*i}"
                    self.app.window_log(text)
                total += 2

                if not self.app.mcu_interactor.click_calibration_button(calibration):  # type: ignore
                    raise AttributeError

                if not self.app.aws_interactor.enable_FPD_calib():
                    raise AttributeError

                text = f"FPD stabilization:"
                self.app.window_log(text)
                for i in range(5):  # type: ignore
                    if self.app.app_state == "stop":
                        raise ConnectionAbortedError
                    sleep(0.5)
                    text = f"FPD stabilization:{'.'*i}"
                    self.app.window_log(text)
                total += 2

                if calibration == "offset" or calibration == "defect":
                    total = self._start_smart_NO_exposure()

                else:
                    total = self.start_smart_loop()
                    print(total)
                    if total == -1:
                        raise ConnectionAbortedError
                    print("end of iteration")

        except ConnectionAbortedError:
            self.app.control.action("stop")
            return

        except AttributeError:
            self.app.messenger.errorMessage()
            self.app.control.action("stop")
            return

        except RuntimeError:
            self.app.messenger.errorMessage()
            self.app.control.action("stop")
            return

        self.app.control.action("stop")
        self.app.messenger.calibrationMessage(total)
        return
