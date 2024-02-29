from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Exposure.constants import *
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import status_mcu
from Exposure.Generic import Generic
from GUI.constants import *


class SmartExposure:
    from GUI.GUI import GUI

    def __init__(self, app: GUI) -> None:
        self.generic = Generic(app)
        self.status_gen: status_gen = "idle"
        self.status_mu: status_mu = "offline"
        self.status_mcu: status_mcu = "offline"
        self.log = app.log
        self.app = app
        self.cv = ComputerVision()
        pass

    def _start_smart_NO_exposure(self) -> int:
        print("NO EXPOSURE CALIBRATION")
        total = 0
        try:
            total += self.generic.wait_calib_end()
            self.app.com.end()
            print("CALIB PASS")
        except RuntimeError:
            return total
        return total

    def start_timer(self) -> int:
        total = 10
        for i in range(total, 0, -1):
            sleep(1)
            self.generic.timerMessage(i)
            if self.app.app_state == "stop":
                raise RuntimeError
        return total

    def start_ma_exposure(self) -> int:
        total = 0
        try:
            self.app.vision.status_label.configure(text="Status: Countdown")  # type: ignore
            total = self.start_timer()
            total += self.generic.wait_standby()
            self.app.vision.status_label.configure(text="Status: Standby")  # type: ignore
            self.app.com.start_long()
            total += self.generic.wait_exposure_start()
            self.app.vision.status_label.configure(text="Status: Under exposure")  # type: ignore
            total += self.generic.wait_exposure_end()
            self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
            self.app.com.end()

        except RuntimeError:
            self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
            return total
        self.generic.exposureMessage(total)
        self.app.control.action("stop")
        return total

    def start_smart_exposure(self) -> int:
        total = 0
        try:
            total += self.generic.wait_standby()
            self.app.vision.status_label.configure(text="Status: Standby")  # type: ignore
            self.app.com.start_short()
            self.app.vision.status_label.configure(text="Status: Under exposure")  # type: ignore
            total += self.generic.wait_exposure_end()
            self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
            self.app.com.end()
        except RuntimeError:
            self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
            return total
        self.generic.exposureMessage(total)
        self.app.control.action("stop")
        return total

    def start_smart_loop(self) -> int:
        total = 0
        exposures = 0
        while True:
            try:
                if self.app.app_state == "stop":
                    raise RuntimeError

                total += self.generic.wait_standby(watchPass=True, count=exposures)
                self.app.vision.status_label.configure(text="Status: Standby")  # type: ignore

                if self.generic.is_calib_passed():
                    self.app.output_log.append("Calib Passed!")
                    self.app.vision.status_label.configure(text="Status: Calib Pass")  # type: ignore
                    break

                self.app.com.start_short()
                total += self.generic.wait_exposure_start()
                self.app.vision.status_label.configure(text="Status: Under exposure")  # type: ignore

                total += self.generic.wait_exposure_end()
                self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
                exposures += 1
                self.app.com.end()

                if self.generic.is_calib_passed():
                    self.app.output_log.append("Calib Passed!")
                    self.app.vision.status_label.configure(text="Status: Calib Pass")  # type: ignore
                    break

            except RuntimeError:
                self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
                self.app.control.action("stop")
                break

        if self.app.app_state != "stop":
            self.generic.setExposureMessage(total, exposures)
            if self.app.mode != "auto":
                self.app.control.action("stop")
        return -1

    def start_auto_loop(self) -> None:
        total = 0
        try:
            for calibration in self.app.selected_cal:

                text = f"Initialization for {calibration} calib"
                sleep(1)
                total += 1

                self.app.output_log.append(text)
                self.app.log("control", "info", text)
                self.app.current_calib = calibration
                self.app.change_current_calib(calibration)

                if not self.app.mcu_interactor.click_calibration_button(calibration):  # type: ignore
                    raise AttributeError

                if not self.app.aws_interactor.enable_FPD_calib():
                    raise AttributeError

                text = f"FPD calibration enabled"
                self.app.output_log.append(text)
                self.app.log("control", "info", text)

                text = f"FPD stabilization for {calibration} calib"
                for i in range(7):
                    if self.app.app_state == "stop":
                        print(i)
                        raise ConnectionAbortedError
                    sleep(0.5)
                total += 3

                self.generic.set_mcu_state("calibrating")
                if calibration == "offset" or calibration == "defect":
                    total = self._start_smart_NO_exposure()

                else:
                    total = self.start_smart_loop()
                    print(total)
                    if total == -1:
                        raise ConnectionAbortedError

        except ConnectionAbortedError:
            self.app.control.action("stop")
            return

        except AttributeError:
            self.generic.errorMessage()
            self.app.control.action("stop")
            return

        except RuntimeError:
            self.generic.errorMessage()
            self.app.control.action("stop")
            return

        self.app.control.action("stop")
        self.generic.calibrationMessage(total)
        return
