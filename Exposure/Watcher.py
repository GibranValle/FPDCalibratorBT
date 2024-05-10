from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Exposure.constants import *
from ComputerVision.ComputerVision import ComputerVision
from GUI.Messenger import Messenger


class Watcher:
    from GUI.GUI import GUI

    def __init__(self, app: GUI) -> None:
        self.app = app
        self.cv = ComputerVision()

    def _view_gen_state(self, button: status_gen) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.app.set_state_gen(button)

    def _view_mu_state(self, button: status_mu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.app.set_state_mu(button)

    def _view_mcu_state(self, button: status_mcu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.app.set_state_mcu(button)

    def wait_calib_end(
        self,
    ) -> int:
        total = 0
        pause = 0
        for i in range(MAX_TIME_STANDBY):
            time = Messenger.convert_seconds(i)
            self.app.window_log(f"Waiting for calib PASS : {time}")
            sleep(SLEEP_TIME)
            total += i

            if self.is_calib_passed():
                time = Messenger.convert_seconds(i)
                self.app.file_log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {time}"
                )
                break
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.app.messenger.pauseMessage(pause)
            elif self.app.app_state == "stop":
                self.app.messenger.abortMessage()
                raise RuntimeError("Aborted requested")
        return total

    def wait_standby(self, watchPass: bool = False, count: int = 0) -> int:
        total = 0
        pause = 0
        for _ in range(MAX_TIME_STANDBY):
            self.app.messenger.standByMessage(total)
            total += 1
            sleep(SLEEP_TIME)
            self.app.messenger.standByMessage(total)
            if watchPass:
                if self.is_calib_passed() and count > 0:
                    break

            if self.app.click_ok:
                clicked = self.app.aws_interactor.click_ok()
                if clicked:
                    self.app.file_log("smart", "info", "button clicked")

            self._view_mu_state("standby")
            self._view_gen_state("push")

            print(self.app.get_state_gen())

            if (
                self.app.get_state_gen() == "push"
                or self.app.get_state_mu() == "standby"
            ):
                time = Messenger.convert_seconds(total)
                self.app.file_log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {time}"
                )
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.app.messenger.pauseMessage(pause)

            elif self.app.app_state == "stop":
                self.app.messenger.abortMessage()
                raise RuntimeError("Aborted requested")

        return total

    def wait_exposure_start(self) -> int:
        total = 0
        pause = 0
        for _ in range(MAX_TIME_BEFORE_EXPOSURE):
            self.app.messenger.startMessage(total)

            if self.is_calib_passed():
                return total

            sleep(SLEEP_TIME / 2)
            total += 1

            self.app.messenger.startMessage(total)

            self._view_mu_state("exposure")

            if self.app.get_state_mu() == "exposure":
                time = Messenger.convert_seconds(total)
                self.app.file_log(
                    "smart", "info", f"xray gen should be exposing, waited: {time}"
                )
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    sleep(1)
                    pause += 1
                    self.app.messenger.pauseMessage(pause)
            elif self.app.app_state == "stop":
                self.app.messenger.abortMessage()
                raise RuntimeError("Aborted requested")

            sleep(SLEEP_TIME / 2)

        return total

    def wait_ma_exposure_start(self) -> int:
        total = 0
        pause = 0
        for _ in range(MAX_TIME_BEFORE_EXPOSURE):
            self.app.messenger.startMessage(total)

            if self.is_calib_passed():
                return total

            sleep(SLEEP_TIME / 2)
            total += 1

            self.app.messenger.startMessage(total)

            self._view_gen_state("exposing")

            if self.app.get_state_gen() == "exposing":
                time = Messenger.convert_seconds(total)
                self.app.file_log(
                    "smart", "info", f"xray gen should be exposing, waited: {time}"
                )
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    sleep(1)
                    pause += 1
                    self.app.messenger.pauseMessage(pause)
            elif self.app.app_state == "stop":
                self.app.messenger.abortMessage()
                raise RuntimeError("Aborted requested")

            sleep(SLEEP_TIME / 2)

        return total

    def wait_exposure_end(self) -> int:
        total = 0
        pause = 0
        for _ in range(MAX_TIME_EXPOSURE):
            self.app.messenger.endMessage(total)

            sleep(SLEEP_TIME / 2)
            total += 1

            self.app.messenger.endMessage(total)

            if self.is_calib_passed():
                return total

            self._view_mu_state("blocked")
            self._view_gen_state("release")

            if self.app.get_state_mu() == "blocked":
                time = Messenger.convert_seconds(total)
                self.app.file_log("watcher", "info", f"end of exposure, waited: {time}")
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.app.messenger.pauseMessage(pause)

            elif self.app.app_state == "stop":
                self.app.messenger.abortMessage()
                raise RuntimeError("Aborted requested")

            sleep(SLEEP_TIME / 2)

        return total

    def wait_ma_exposure_end(self) -> int:
        total = 0
        pause = 0
        for _ in range(MAX_TIME_EXPOSURE):
            self.app.messenger.endMessage(total)

            sleep(SLEEP_TIME / 2)
            total += 1

            if self.is_calib_passed():
                return total

            self.app.messenger.endMessage(total)

            self._view_gen_state("release")

            if self.app.get_state_gen() == "release":
                time = Messenger.convert_seconds(total)
                self.app.file_log("watcher", "info", f"end of exposure, waited: {time}")
                break

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    sleep(1)
                    pause += 1
                    self.app.messenger.pauseMessage(pause)

            elif self.app.app_state == "stop":
                self.app.messenger.abortMessage()
                raise RuntimeError("Aborted requested")

            sleep(SLEEP_TIME / 2)

        return total

    def is_calib_passed(self) -> bool:
        self._view_mcu_state("pasar")
        self._view_mcu_state("saltar")
        if self.app.get_state_mcu() == "pasar" or self.app.get_state_mcu() == "saltar":
            self.app.statusBox.status_mcu_label.configure(text=f"MCU: {self.app.get_state_mcu()}")  # type: ignore
            self.app.file_log("smart", "info", f"Calib passed")
            return True
        return False
