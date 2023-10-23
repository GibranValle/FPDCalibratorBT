from typing import Any
from ComputerVision.cv_types import status_gen, status_mcu, status_mu
from time import sleep
from SmartExposure.constants import *
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

    def _get_gen_state(self) -> None:
        print(self.cv.get_gen_status())
        self.status_gen = self.cv.get_gen_status()

    def _get_mu_state(self) -> None:
        print(self.cv.get_mu_status())
        self.status_mu = self.cv.get_mu_status()

    def _get_mcu_state(self) -> None:
        print(self.cv.get_mcu_status())
        self.status_mcu = self.cv.get_mcu_status()

    def start_smart_exposure(self):
        total = 0
        print(self.app.app_state)
        for i in range(MAX_TIME_STANDBY):
            sleep(SLEEP_TIME)
            self._get_mu_state()
            self._get_gen_state()
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
            self._get_mu_state()
            self._get_gen_state()
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
            self._get_mu_state()
            self._get_gen_state()
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
