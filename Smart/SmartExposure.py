from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Smart.constants import *
from ComputerVision.ComputerVision import ComputerVision


class SmartExposure:
    from GUI.GUI import GUI

    def __init__(self, app: GUI) -> None:
        self.status_gen: status_gen = "idle"
        self.status_mu: status_mu = "offline"
        self.status_mcu: status_mcu = "offline"
        self.log = app.log
        self.output = app.output
        self.app = app
        self.cv = ComputerVision()
        pass

    def _get_gen_state(self, button: status_gen) -> None:
        x, y = self.cv.get_icon_coords_status_gen(button)
        if x > 0 and y > 0:
            self.status_gen = button
        else:
            self.status_gen = "idle"

    def _get_mu_state(self, button: status_mu) -> None:
        x, y = self.cv.get_icon_coords_status_mu(button)
        if x > 0 and y > 0:
            self.status_mu = button
        else:
            self.status_mu = "offline"

    def _get_mcu_state(self, button: status_mcu) -> None:
        x, y = self.cv.get_icon_coords_status_mcu(button)
        if x > 0 and y > 0:
            self.status_mcu = button
        else:
            self.status_mu = "offline"

    def wait_standby(self, exposure: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_STANDBY):
            sleep(SLEEP_TIME)
            self._get_mu_state("standby")
            self._get_gen_state("push")
            self.output.waiting_ready(i)
            if exposure > 0 and self.is_calib_passed():
                return i
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted(i)
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "push" or self.status_mu == "standby":
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
            total += i
        return total

    def wait_exposure_start(self, exposure: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_BEFORE_EXPOSURE):
            sleep(SLEEP_TIME)
            self._get_mu_state("exposure")
            self._get_gen_state("exposing")
            self.output.waiting_exposure_start(i)
            if exposure > 0 and self.is_calib_passed():
                return i
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted(i)
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "exposing" or self.status_mu == "exposure":
                self.log("smart", "info", f"xray gen should be exposing, waited: {i}")
                break
            total += i
        return total

    def wait_exposure_end(self, exposure: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_EXPOSURE):
            sleep(SLEEP_TIME)
            self._get_mu_state("blocked")
            self._get_gen_state("release")
            self.output.waiting_exposure_end(i)
            if exposure > 0 and self.is_calib_passed():
                return i
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted(i)
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "release" or self.status_mu == "blocked":
                self.log("smart", "info", f"end of exposure, waited: {i}")
                break
            total += i
        return total

    def is_calib_passed(self) -> bool:
        self._get_mcu_state("pasar")
        self._get_mcu_state("saltar")
        if self.status_mcu == "pasar" or self.status_mcu == "saltar":
            return True
        return False

    def start_smart_exposure(self):
        self.output.clear_all()
        total = 0
        try:
            total += self.wait_standby()
            total += self.wait_exposure_start()
            total += self.wait_exposure_end()
        except RuntimeError:
            self.app.change_app_state("stop")
            self.output.exposure_aborted(total)
            return
        self.output.waiting_exposure_end(total)
        self.app.change_app_state("stop")

    def start_smart_loop(self):
        print("smart loop")
        self.output.clear_all()
        total = 0
        exposures = 0
        while True:
            try:
                total += self.wait_standby(exposures)
                if self.is_calib_passed():
                    break
            except RuntimeError:
                self.output.exposure_aborted(total)
                break
            try:
                total += self.wait_exposure_start(exposures)
                if self.is_calib_passed():
                    break
            except RuntimeError:
                self.output.exposure_aborted(total)
                break

            try:
                total += self.wait_exposure_end(exposures)
                if self.is_calib_passed():
                    break
                exposures += 1
            except RuntimeError:
                self.output.exposure_aborted(total)
                break
        self.app.change_app_state("stop")
