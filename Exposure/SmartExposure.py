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
        except RuntimeError:
            return total
        return total

    def start_timer(self, init: int = 5, end: int = -1) -> int:
        total = 0
        pause = 0
        for i in range(init, end, -1 if init > end else 1):
            self.app.messenger.timerMessage(i)
            sleep(1)
            total += 1
            if self.app.app_state == "stop":
                raise RuntimeError
            elif self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.app.messenger.pauseMessage(pause)
        return total

    def start_ma_exposure(self) -> int:
        total = 0
        try:
            self.app.statusBox.status_gen_label.configure(text="Gen: Countdown", text_color="white")  # type: ignore
            total += self.start_timer()
            total += self.app.watcher.wait_standby()
            self.app.statusBox.status_gen_label.configure(text="Gen: Standby", text_color="white")  # type: ignore
            self.app.com.start_long()
            total += self.app.watcher.wait_ma_exposure_start()
            self.app.statusBox.status_gen_label.configure(text="Gen: Under exposure", text_color="yellow")  # type: ignore
            total += self.app.watcher.wait_ma_exposure_end()
            self.app.statusBox.status_gen_label.configure(text="Gen: Blocked", text_color="red")  # type: ignore
            self.app.com.end()

        except RuntimeError:
            self.app.com.end()
            self.app.statusBox.status_gen_label.configure(text="Gen: Blocked", text_color="red")  # type: ignore
            return total
        self.app.messenger.exposureMessage(total)
        self.app.control.action("stop")
        return total

    def start_manual_continuos(
        self, duration: dur_option = "short 5s", pause: int = 30
    ) -> int:
        total = 0
        exposures = 0
        exposure = 5 if duration == "short 5s" else 15
        self.app.messenger.separator()
        while True:
            try:
                if self.app.app_state == "stop":
                    raise RuntimeError
                self.app.window_log(f"MC: Requesting exposure - {exposures +1}")
                self.app.com.start_short()
                self.app.window_log(f"MC: Accepted exposure - {exposures + 1}")
                self.app.statusBox.status_mu_label.configure(text="MU: Under exposure", text_color="yellow")  # type: ignore
                total += self.start_timer(0, exposure + 1)

                self.app.window_log(f"MC: Requesting end - {exposures +1}")
                self.app.com.end()
                self.app.window_log(f"MC: Accepted end exposure - {exposures+1}")
                self.app.statusBox.status_mu_label.configure(text="MU: Standby", text_color="white")  # type: ignore
                total += self.start_timer(0, pause + 1)
                exposures += 1

            except RuntimeError:
                self.app.com.end()
                if exposures > 0:
                    self.app.messenger.setExposureMessage(total, exposures)
                else:
                    self.app.messenger.abortMessage()
                self.app.statusBox.status_mu_label.configure(text="MU: Blocked", text_color="red")  # type: ignore
                self.app.control.action("stop")
                return total

    def start_smart_exposure(self) -> int:
        total = 0
        try:
            total += self.app.watcher.wait_standby()
            self.app.statusBox.status_mu_label.configure(text="MU: Standby", text_color="white")  # type: ignore
            self.app.com.start_short()
            self.app.statusBox.status_mu_label.configure(text="MU: Under exposure", text_color="yellow")  # type: ignore
            total += self.app.watcher.wait_exposure_end()
            self.app.statusBox.status_mu_label.configure(text="MU: Blocked", text_color="red")  # type: ignore
            self.app.com.end()
        except RuntimeError:
            self.app.com.end()
            self.app.statusBox.status_mu_label.configure(text="MU: Blocked", text_color="red")  # type: ignore
            return total
        self.app.messenger.exposureMessage(total)
        self.app.control.action("stop")
        return total

    def start_smart_loop(self) -> int:
        total = 0
        exposures = 0
        self.app.set_state_mcu("idle")
        self.app.statusBox.status_mcu_label.configure(text="MCU: calibrating")  # type: ignore
        while True:
            try:
                if self.app.app_state == "stop":
                    raise RuntimeError

                total += self.app.watcher.wait_standby(watchPass=True, count=exposures)
                self.app.statusBox.status_mu_label.configure(text="MU: Standby", text_color="white")  # type: ignore

                if self.app.watcher.is_calib_passed():
                    self.app.window_log("Calib Passed!")
                    self.app.set_state_mcu("pasar")
                    self.app.statusBox.status_mu_label.configure(text="MU: Calib Pass", text_color="green")  # type: ignore
                    break

                self.app.com.start_short()
                total += self.app.watcher.wait_exposure_start()
                self.app.statusBox.status_mu_label.configure(text="MU: Under exposure", text_color="yellow")  # type: ignore

                total += self.app.watcher.wait_exposure_end()
                self.app.statusBox.status_mu_label.configure(text="MU: Blocked", text_color="red")  # type: ignore
                exposures += 1
                self.app.com.end()

                if self.app.watcher.is_calib_passed():
                    self.app.window_log("Calib Passed!")
                    self.app.set_state_mcu("pasar")
                    self.app.statusBox.status_mu_label.configure(text="MU: Calib Pass", text_color="green")  # type: ignore
                    break

            except RuntimeError:
                self.app.com.end()
                self.app.set_state_mcu("idle")
                self.app.statusBox.status_mu_label.configure(text="MU: Blocked", text_color="red")  # type: ignore
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
                    if total == -1:
                        raise ConnectionAbortedError

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
