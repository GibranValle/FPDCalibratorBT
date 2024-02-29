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

    def errorMessage(self):
        self.app.output_log.append(f"Aborted!")
        self.log("smart", "error", "Error")

    def abortMessage(self):
        self.app.output_log.append(f"Aborted!")
        self.log("smart", "error", "request of abortion")

    def timerMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Countdown: {time}")

    def standByMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Waiting for exposure ready: {time}")

    def startMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Waiting for exposure start: {time}")

    def endMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Waiting for exposure end: {time}")

    def calibrationMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Calibration completed!\nTotal time: {time}")
        self.log("smart", "success", f"Calibration completed!\nTotal time: {time}")

    def underExpMessage(self, seconds: int, isLong: bool = False):
        time = self.convert_seconds(seconds)
        a = "LONG" if isLong else ""
        self.app.output_log.append(f"Under {a} exposure: {time}")

    def exposureMessage(self, seconds: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(f"Exposure completed!\nTotal time: {time}")
        self.log("smart", "success", f"Exposure completed!\nTotal time: {time}")

    def setExposureMessage(self, seconds: int, exposures: int):
        time = self.convert_seconds(seconds)
        self.app.output_log.append(
            f"{exposures} exposures completed!\nTotal time: {time}"
        )
        self.log(
            "smart", "success", f"{exposures} exposures completed!\nTotal time: {time}"
        )

    def __init__(self, app: GUI) -> None:
        self.status_gen: status_gen = "idle"
        self.status_mu: status_mu = "offline"
        self.status_mcu: status_mcu = "offline"
        self.log = app.log
        self.app = app
        self.cv = ComputerVision()
        pass

    def _get_gen_state(self, button: status_gen) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_gen = button

    def _get_mu_state(self, button: status_mu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_mu = button

    def _get_mcu_state(self, button: status_mcu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_mcu = button

    def set_mcu_state(self, button: status_mcu) -> None:
        self.status_mcu = button

    def wait_calib_start(
        self,
        calibration: status_mcu,
        exposure: int = 0
    ) -> int:
        if exposure > 0:
            return 0
        total = 0
        pause = 0
        for i in range(MAX_TIME_STANDBY):
            sleep(SLEEP_TIME)
            self._get_mcu_state(calibration)
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.pauseMessage(pause)
            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")
            elif self.status_mcu == calibration:
                time = self.convert_seconds(i)
                self.app.output_log.append(
                    f"X ray gen is ready for exposure waited: {time}"
                )
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {time}"
                )
                break
            total += i
        return total

    def wait_calib_end(
        self,
    ) -> int:
        total = 0
        pause = 0
        for i in range(MAX_TIME_STANDBY):
            time = self.convert_seconds(i)
            self.app.output_log.append(f"Waiting for calib PASS : {time}")
            sleep(SLEEP_TIME)
            total += i

            if self.is_calib_passed():
                time = self.convert_seconds(i)
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {time}"
                )
                break
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.pauseMessage(pause)
            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")
        return total

    def wait_standby(self, watchPass: bool = False, count: int = 0) -> int:
        total = 0
        pause = 0
        for i in range(MAX_TIME_STANDBY):
            self.standByMessage(i)
            sleep(SLEEP_TIME)
            total += 1

            if watchPass:
                if self.is_calib_passed() and count > 0:
                    break

            if self.app.click_ok:
                clicked = self.app.aws_interactor.click_ok()
                if clicked:
                    self.app.output_log.append(f"Clicked ok button")
                    self.log("smart", "info", "button clicked")

            self._get_mu_state("standby")
            self._get_gen_state("push")

            if self.status_gen == "push" or self.status_mu == "standby":
                time = self.convert_seconds(i)
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {time}"
                )
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.pauseMessage(pause)

            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")

        return total

    def wait_exposure_start(self) -> int:
        total = 0
        pause = 0
        for i in range(MAX_TIME_BEFORE_EXPOSURE):
            self.startMessage(i)

            if self.is_calib_passed():
                return total

            sleep(SLEEP_TIME / 2)
            total += i

            self._get_mu_state("exposure")
            self._get_gen_state("exposing")

            if self.status_gen == "exposing" or self.status_mu == "exposure":
                time = self.convert_seconds(i)
                self.log(
                    "smart", "info", f"xray gen should be exposing, waited: {time}"
                )
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    sleep(1)
                    pause += 1
                    self.pauseMessage(pause)
            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")

            sleep(SLEEP_TIME / 2)

        return total

    def wait_exposure_end(self) -> int:
        total = 0
        pause = 0
        for i in range(MAX_TIME_EXPOSURE):
            self.endMessage(i)

            sleep(SLEEP_TIME / 2)
            total += 1

            if self.is_calib_passed():
                return total

            self._get_mu_state("blocked")
            self._get_gen_state("release")

            if self.status_gen == "release" or self.status_mu == "blocked":
                time = self.convert_seconds(i)
                self.log("generic", "info", f"end of exposure, waited: {time}")
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.pauseMessage(pause)

            elif self.app.app_state == "stop":
                self.abortMessage()
                raise RuntimeError("Aborted requested")

            sleep(SLEEP_TIME / 2)

        return total

    def is_calib_passed(self) -> bool:
        self._get_mcu_state("pasar")
        self._get_mcu_state("saltar")
        if self.status_mcu == "pasar" or self.status_mcu == "saltar":
            self.log("smart", "info", f"Calib passed")
            return True
        return False
