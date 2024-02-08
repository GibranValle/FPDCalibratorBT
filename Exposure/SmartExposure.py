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
            total += self.generic.wait_calib_pass()
            self.app.com.end()
            print("CALIB PASS")
        except RuntimeError:
            self.generic.abortMessage()
            return total
        return total

    def start_timer(self) -> int:
        total = 10
        for i in range(total, 0, -1):
            sleep(1)
            self.generic.timerMessage(i)
        return total

    def start_smart_exposure(self, timer: bool = False) -> int:
        total = 0
        try:
            if timer and total == 0:
                self.app.vision.status_label.configure(text="Status: Countdown")  # type: ignore
                total = self.start_timer()

            total += self.generic.wait_standby()
            self.app.vision.status_label.configure(text="Status: Standby")  # type: ignore
            if timer:
                print("LONG EXPOSURE")
                self.app.com.start_long()
            else:
                self.app.com.start_short()
            total += self.generic.wait_exposure_start()
            self.app.vision.status_label.configure(text="Status: Under exposure")  # type: ignore
            total += self.generic.wait_exposure_end()
            self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
            self.app.com.end()
        except RuntimeError:
            self.generic.abortMessage()
            self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
            return total
        self.generic.exposureMessage(total)
        return total

    def start_smart_loop(self, variant: exposure_option = "short") -> int:
        # for semi mode
        total = 0
        exposures = 0
        while True:
            try:
                total += self.generic.wait_standby(count=exposures)
                self.app.vision.status_label.configure(text="Status: Standby")  # type: ignore
                self.app.com.start_short()
                if variant == "short":
                    total += self.generic.wait_exposure_start()
                self.app.vision.status_label.configure(text="Status: Under exposure")  # type: ignore
                total += self.generic.wait_exposure_end()
                self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
                self.app.com.end()
                exposures += 1
                if self.generic.is_calib_passed():
                    self.app.vision.status_label.configure(text="Status: Calib passed")  # type: ignore
                    break
            except RuntimeError:
                self.app.change_app_state("stop")
                self.generic.abortMessage()
                self.app.vision.status_label.configure(text="Status: Blocked")  # type: ignore
                break
        self.generic.setExposureMessage(total, exposures)
        self.app.change_app_state("stop")
        return total

    def start_auto_loop(self, variant: exposure_option = "short"):
        total = 0
        try:
            for calibration in self.app.selected_cal:
                if self.app.app_state == "stop":
                    raise ConnectionAbortedError

                text = f"Stabilization for {calibration} calib"
                self.app.output_log.append(text)
                self.app.log("control", "info", text)
                self.app.current_calib = calibration
                self.app.change_current_calib(calibration)

                sleep(2)
                total += 2

                if not self.app.mcu_interactor.click_calibration_button(calibration):  # type: ignore
                    raise AttributeError

                if not self.app.aws_interactor.enable_FPD_calib():
                    raise AttributeError

                text = f"FPD calibration enabled"
                self.app.output_log.append(text)
                self.app.log("control", "info", text)

                if calibration == "offset" or calibration == "defect":
                    total = self._start_smart_NO_exposure()

                else:
                    total = self.start_smart_loop(variant)

        except ConnectionAbortedError:
            self.generic.abortMessage()
            self.app.control.action("stop")

        except AttributeError:
            self.app.control.action("stop")

        except RuntimeError:
            self.app.control.action("stop")

        else:
            self.app.control.action("stop")
            self.generic.calibrationMessage(total)
