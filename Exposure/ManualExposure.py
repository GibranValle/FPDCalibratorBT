from time import sleep
from Exposure.constants import *
from GUI.constants import *


class ManualExposure:
    from GUI.GUI import GUI

    def __init__(self, app: GUI) -> None:
        self.app = app
        pass

    # -------------------- MANUAL OPERATIONS ----------------------------------------
    def start_exposure(self, variant: exposure_option = "short"):
        try:
            if variant == "short":
                self.app.window_log("Requesting start of exposure")
                self.app.com.start_short()
                self.app.window_log("Accepted start of exposure")
            elif variant == "long":
                self.app.window_log("Requesting start of LONG exposure")
                self.app.com.start_long()
                self.app.window_log("Accepted start of LONG exposure")
        except ConnectionAbortedError:
            return

        try:
            if variant == "short":
                for i in range(SHORT_TIME_EXPOSURE + 1):
                    if self.app.app_state == "stop":
                        raise StopIteration
                    sleep(1)
                    self.app.messenger.underExpMessage(i, False)
            else:
                for i in range(LONG_TIME_EXPOSURE + 1):
                    if self.app.app_state == "stop":
                        raise StopIteration
                    sleep(1)
                    self.app.messenger.underExpMessage(i, True)
            try:
                sleep(0.3)
                self.app.com.end()
            except ConnectionAbortedError:
                return
        except StopIteration:
            self.app.change_app_state("stop")
            self.app.control.action("stop")
            self.app.com.end()
            self.app.window_log("Exposure Aborted!\n-----------------------")
            return
        self.app.change_app_state("stop")
        self.app.control.action("stop")
        self.app.com.end()
        self.app.window_log("Exposure completed!\n-----------------------")