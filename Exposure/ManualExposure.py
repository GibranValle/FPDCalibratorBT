from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Exposure.constants import *
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import status_mcu
from Exposure.Generic import Generic
from GUI.constants import *


class ManualExposure:
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

    # -------------------- MANUAL OPERATIONS ----------------------------------------
    def start_exposure(self, variant: exposure_option = "short"):
        try:
            if variant == "short":
                self.app.output_log.append("Requesting start of exposure")
                self.app.com.start_short()
                self.app.output_log.append("Accepted start of exposure")
            elif variant == "long":
                self.app.output_log.append("Requesting start of LONG exposure")
                self.app.com.start_long()
                self.app.output_log.append("Accepted start of LONG exposure")
        except ConnectionAbortedError:
            return

        try:
            for i in range(LONG_TIME_EXPOSURE + 1):
                if self.app.app_state == "stop":
                    raise StopIteration
                sleep(1)
                self.generic.underExpMessage(i, variant == "long")
            try:
                sleep(0.3)
                self.app.com.end()
            except ConnectionAbortedError:
                return
        except StopIteration:
            self.app.change_app_state("stop")
            self.app.control.action("stop")
            self.app.com.end()
            self.app.output_log.append("Exposure Aborted!\n-----------------------")
            return
        self.app.change_app_state("stop")
        self.app.control.action("stop")
        self.app.com.end()
        self.app.output_log.append("Exposure completed!\n-----------------------")

    def end_exposure(self):
        sleep(1)
        try:
            sleep(0.3)
            self.app.com.end()
        except ConnectionAbortedError:
            return
        self.app.output_log.append("Error: Exposure canceled!\n-----------------------")
