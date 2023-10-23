from typing import Any
from ComputerVision.cv_types import status_gen, status_mcu, status_mu
from time import sleep
from Smart.constants import *
from ComputerVision.ComputerVision import ComputerVision


class SmartExposure:
    def __init__(self, app: Any) -> None:
        self.status_gen: status_gen = "idle"
        self.status_mcu: status_mcu = "offline"
        self.status_mu: status_mu = "offline"
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
            self.status_mcu = "offline"

    def start_smart_exposure(self):
        total = 0
        print(self.app.app_state)

        for i in range(MAX_TIME_STANDBY):
            sleep(SLEEP_TIME)
            self._get_mu_state("standby")
            self._get_gen_state("push")
            self.output.waiting_ready(i)
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted(i)
                return
            elif self.status_gen == "push" or self.status_mu == "standby":
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
            total += i

        for i in range(MAX_TIME_BEFORE_EXPOSURE):
            sleep(SLEEP_TIME)
            self._get_mu_state("exposure")
            self._get_gen_state("exposing")
            self.output.waiting_exposure_start(i)
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted(i)
                return
            elif self.status_gen == "exposing" or self.status_mu == "exposure":
                self.log("smart", "info", f"xray gen should be exposing, waited: {i}")
                break
            total += i

        for i in range(MAX_TIME_EXPOSURE):
            sleep(SLEEP_TIME)
            self._get_mu_state("blocked")
            self._get_gen_state("release")
            self.output.waiting_exposure_end(i)
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted(i)
                return
            elif self.status_gen == "release" or self.status_mu == "blocked":
                self.log("smart", "info", f"end of exposure, waited: {i}")
                break
            total += i
        self.output.waiting_exposure_end(total)
        self.app.change_state("stop")
