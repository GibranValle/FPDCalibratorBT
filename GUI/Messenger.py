from Exposure.constants import *
from ComputerVision.ComputerVision import ComputerVision
from GUI.constants import class_option

class Messenger:
    from GUI.GUI import GUI

    @staticmethod
    def convert_seconds(secs: int) -> str:
        temp = secs
        if secs >= 3600:
            hours = int(secs / 3600)
            temp -= secs - 3600 * hours
            mins = int(temp / 60)
            sec = temp % 60
            return f"{hours}h {mins}m {sec}s"
        if secs >= 60:
            mins = int(secs / 60)
            sec = secs % 60
            return f"{mins}m {sec}s"
        return f"{secs}s"

    def pauseMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(f"In pause: {time}")

    def errorMessage(self, _class: class_option = 'messenger'):
        self.app.window_log(f"Aborted!")
        self.log(_class, "error", "Error")

    def abortMessage(self):
        self.app.window_log(f"Aborted!")
        self.log("smart", "error", "request of abortion")

    def timerMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(f"Countdown: {time}")

    def standByMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(f"Waiting for exposure ready: {time}")

    def startMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(f"Waiting for exposure start: {time}")

    def endMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(f"Waiting for exposure end: {time}")

    def calibrationMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(f"Calibration completed!\nTotal time: {time}")
        self.log("smart", "success", f"Calibration completed!\nTotal time: {time}")

    def underExpMessage(self, seconds: int, isLong: bool = False):
        time = self.convert_seconds(seconds)
        a = "LONG" if isLong else ""
        self.app.window_log(f"Under {a} exposure: {time}")

    def exposureMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(f"Exposure completed!\nTotal time: {time}")
        self.log("smart", "success", f"Exposure completed!\nTotal time: {time}")

    def setExposureMessage(self, seconds: int, exposures: int):
        time = self.convert_seconds(seconds)
        self.app.window_log(
            f"{exposures} exposures completed!\nTotal time: {time}"
        )
        self.log(
            "smart", "success", f"{exposures} exposures completed!\nTotal time: {time}"
        )

    def __init__(self, app: GUI) -> None:
        self.log = app.file_log
        self.app = app
        self.cv = ComputerVision()
        