from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Exposure.constants import *
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import status_mcu
from GUI.constants import BASIC_CALIBRATIONS
from Exposure.Generic import Generic


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

    def _start_smart_exposure(self) -> int:
        # for semi mode
        total = 0
        try:
            total += self.generic.wait_standby()
            self.app.com.start(variant="short")
            total += self.generic.wait_exposure_start()
            total += self.generic.wait_exposure_end()
            self.app.com.end()
        except RuntimeError:
            self.generic.abortMessage()
            return total
        self.generic.exposureMessage(total)
        self.app.change_app_state("stop")
        self.app.control.action("stop")
        return total

    def _start_smart_NO_exposure(self) -> int:
        # for semi mode
        total = 0
        try:
            total += self.generic.wait_calib_pass()
            self.app.com.end()
        except RuntimeError:
            self.generic.abortMessage()
            return total
        self.generic.exposureMessage(total)
        self.app.change_app_state("stop")
        self.app.control.action("stop")
        return total

    def start_smart_loop(self) -> int:
        # for semi mode
        total = 0
        exposures = 0
        while True:
            try:
                total += self.generic.wait_standby(count=exposures)
                self.app.com.start(variant="short")
                total += self.generic.wait_exposure_start()
                total += self.generic.wait_exposure_end()
                self.app.com.end()
                exposures += 1
                if self.generic.is_calib_passed():
                    break
            except RuntimeError:
                self.app.change_app_state("stop")
                self.generic.abortMessage()
                break
        self.generic.setExposureMessage(total, exposures)
        self.app.change_app_state("stop")
        return total

    def start_auto_loop(self):
        total = 0
        try:
            for calibration in self.app.selected_cal:
                if calibration == "offset" or calibration == "defect":
                    self.app.output.change_a(f"Starting {calibration} calib")
                    self.app.output.change_b(f"Stabilizing...")
                    sleep(2)
                    total += 2
                    self.app.output.change_b(f"No exposure required")
                    if not self.app.mcu_interactor.click_calibration_button(
                        calibration
                    ):
                        raise AttributeError
                    if not self.app.aws_interactor.enable_FPD_calib():
                        raise AttributeError
                    total = self._start_smart_NO_exposure()
                elif calibration in BASIC_CALIBRATIONS:
                    self.app.output.change_a(f"Starting {calibration} calib")
                    self.app.output.change_b(f"Stabilizing...")
                    sleep(2)
                    total += 2
                    self.app.mcu_interactor.click_calibration_button(calibration)
                    self.app.aws_interactor.enable_FPD_calib()
                total = self._start_smart_NO_exposure()
        except AttributeError:
            print("aborted")
            self.app.output.icon_not_found()
        except RuntimeError:
            print("aborted")
            self.app.output.calibration_aborted()
        else:
            print("Completed!")
            self.app.output.calibration_success(total)
