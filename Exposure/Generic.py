from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Exposure.constants import *
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import status_mcu


class Generic:
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
        self.app.output_log.append(f"In pause: {time}")

    def abortMessage(self):
        self.app.output_log.append(f"Aborted!")
        self.log("smart", "error", "request of abortion")

    def startMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Waiting for exposure start: {time}")

    def endMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Waiting for exposure end: {time}")

    def calibrationMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Calibration completed! total time: {time}")

    def underExpMessage(self, seconds: int, isLong: bool = False):
        time = self.convert_seconds(seconds)
        a = "LONG" if isLong else ""
        self.app.output_log.append(f"Under {a} exposure: {time}")

    def exposureMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Exposure completed! total time: {time}")

    def setExposureMessage(self, seconds: int, exposures: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(
            f"{exposures} exposures completed! total time: {time}"
        )

    def __init__(self, app: GUI) -> None:
        self.status_gen: status_gen = "idle"
        self.status_mu: status_mu = "offline"
        self.status_mcu: status_mcu = "offline"
        self.log = app.log
        self.app = app
        self.cv = ComputerVision()
        pass

    def get_gen_state(self, button: status_gen) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_gen = button
        else:
            self.status_gen = "idle"

    def get_mu_state(self, button: status_mu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_mu = button
        else:
            self.status_mu = "offline"

    def get_mcu_state(self, button: status_mcu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_mcu = button
        else:
            self.status_mcu = "offline"

    def wait_calib_start(
        self,
        calibration: status_mcu,
        exposure: int = 0,
    ) -> int:
        if exposure > 0:
            return 0
        total = 0
        for i in range(MAX_TIME_STANDBY):
            sleep(SLEEP_TIME)
            self.get_mcu_state(calibration)
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.pauseMessage(i)
            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")
            elif self.status_mcu == calibration:
                self.app.output_log.append(
                    f"X ray gen is ready for exposure waited: {i} timeunits"
                )
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
            total += i
        return total

    def wait_calib_end(
        self,
    ) -> int:
        total = 0
        for i in range(MAX_TIME_STANDBY):
            self.app.output_log.append(f"Waiting for calib end: {i} timeunits")
            sleep(SLEEP_TIME)
            if self.is_calib_passed():
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.pauseMessage(i)
            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")
            total += i
        return total

    def wait_standby(self, count: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_STANDBY):
            if count > 0:
                if self.is_calib_passed():
                    break

            self.get_mu_state("standby")
            self.get_gen_state("push")
            self.app.output_log.append(f"Waiting for exposure: {i} timeunits")
            sleep(SLEEP_TIME)
            total += 1

            if self.app.click_ok:
                self.app.output_log.append(f"Clicked ok button")
                self.log("smart", "info", "button clicked")

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.pauseMessage(i)

            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")

            elif self.status_gen == "push" or self.status_mu == "standby":
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
        return total

    def wait_exposure_start(self) -> int:
        total = 0
        for i in range(MAX_TIME_BEFORE_EXPOSURE):
            if self.is_calib_passed():
                return total

            self.get_mu_state("exposure")
            self.get_gen_state("exposing")
            self.startMessage(i)
            sleep(SLEEP_TIME)
            total += i
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.pauseMessage(i)
            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "exposing" or self.status_mu == "exposure":
                self.log("smart", "info", f"xray gen should be exposing, waited: {i}")
                break
        return total

    def wait_exposure_end(self) -> int:
        total = 0
        for i in range(MAX_TIME_EXPOSURE):
            if self.is_calib_passed():
                return total

            self.get_mu_state("blocked")
            self.get_gen_state("release")
            self.endMessage(i)
            sleep(SLEEP_TIME)
            total += 1

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.pauseMessage(i)

            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")

            elif self.status_gen == "release" or self.status_mu == "blocked":
                self.log("smart", "info", f"end of exposure, waited: {i}")
                break
        return total

    def wait_calib_pass(self) -> int:
        total = 0
        for i in range(MAX_TIME_EXPOSURE):
            if self.is_calib_passed():
                return i
            sleep(SLEEP_TIME)
            total = i
        return total

    def is_calib_passed(self) -> bool:
        self.get_mcu_state("pasar")
        if self.status_mcu == "pasar":
            return True
        return False
