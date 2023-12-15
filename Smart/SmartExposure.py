from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Smart.constants import *
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import status_mcu
from GUI.constants import BASIC_CALIBRATIONS


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
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_gen = button
        else:
            self.status_gen = "idle"

    def _get_mu_state(self, button: status_mu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_mu = button
        else:
            self.status_mu = "offline"

    def _get_mcu_state(self, button: status_mcu) -> None:
        x, y = self.cv.get_status(button)
        if x > 0 and y > 0:
            self.status_mcu = button
        else:
            self.status_mcu = "offline"

    def _wait_calib_start(
        self,
        calibration: status_mcu,
        exposure: int = 0,
    ) -> int:
        if exposure > 0:
            return 0
        total = 0
        for i in range(MAX_TIME_STANDBY):
            self.output.waiting_calib_start(i)
            sleep(SLEEP_TIME)
            self._get_mcu_state(calibration)
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.output.in_pause(i)
            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_mcu == calibration:
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
            total += i
        return total

    def _wait_calib_end(
        self,
    ) -> int:
        total = 0
        for i in range(MAX_TIME_STANDBY):
            self.output.waiting_calib_end(i)
            sleep(SLEEP_TIME)
            if self._is_calib_passed():
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.output.in_pause(i)
            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            total += i
        return total

    def _wait_standby(self, count: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_STANDBY):
            if count > 0:
                if self._is_calib_passed():
                    break

            self._get_mu_state("standby")
            self._get_gen_state("push")
            self.output.waiting_ready(i)
            sleep(SLEEP_TIME)
            total += 1

            if self.app.aws_interactor.click_ok():
                self.output.change_a("button clicked!")
                self.log("smart", "info", "button clicked")

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.output.in_pause(i)

            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")

            elif self.status_gen == "push" or self.status_mu == "standby":
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
        return total

    def _wait_exposure_start(self) -> int:
        total = 0
        for i in range(MAX_TIME_BEFORE_EXPOSURE):
            if self._is_calib_passed():
                return total

            self._get_mu_state("exposure")
            self._get_gen_state("exposing")
            self.output.waiting_exposure_start(i)
            sleep(SLEEP_TIME)
            total += i
            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.output.in_pause(i)
            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "exposing" or self.status_mu == "exposure":
                self.log("smart", "info", f"xray gen should be exposing, waited: {i}")
                break
        return total

    def _wait_exposure_end(self) -> int:
        total = 0
        for i in range(MAX_TIME_EXPOSURE):
            if self._is_calib_passed():
                return total

            self._get_mu_state("blocked")
            self._get_gen_state("release")
            self.output.waiting_exposure_end(i)
            sleep(SLEEP_TIME)
            total += 1

            if self.app.app_state == "pause":
                while self.app.app_state == "pause":
                    if self.app.app_state != "pause":
                        break
                    self.output.in_pause(i)

            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")

            elif self.status_gen == "release" or self.status_mu == "blocked":
                self.log("smart", "info", f"end of exposure, waited: {i}")
                break
        return total

    def _wait_calib_pass(self) -> int:
        total = 0
        for i in range(MAX_TIME_EXPOSURE):
            if self._is_calib_passed():
                return i
            sleep(SLEEP_TIME)
            total = i
        return total

    def _is_calib_passed(self) -> bool:
        self._get_mcu_state("pasar")
        if self.status_mcu == "pasar":
            return True
        return False

    # -------------------- EXPORTED ----------------------------------------
    def start_short_exposure(self):
        try:
            self.app.output.clear_all()
            self.app.output.change_a("Requesting start of exposure")
            sleep(0.3)
            self.app.com.start(variant="short")
            self.app.output.change_a("Accepted start of exposure")
        except ConnectionAbortedError:
            return

        for i in range(SHORT_TIME_EXPOSURE + 1):
            if self.app.app_state == "stop":
                return
            sleep(1)
            self.app.output.change_b(f"Under exposure: {i}")

        try:
            self.app.output.clear_all()
            self.app.output.change_a("Requesting end of exposure")
            sleep(0.3)
            self.app.com.end()
            self.app.output.change_a("Accepted end of exposure")
        except ConnectionAbortedError:
            return

        self.app.output.change_a(f"Exposure Completed!")
        self.app.output.change_b(f"------------------------------")

    def start_long_exposure(self):
        try:
            self.app.output.clear_all()
            self.app.output.change_a("Requesting start of LONG exposure")
            sleep(0.3)
            self.app.com.start(variant="long")
            self.app.output.change_a("Accepted start of LONG exposure")
        except ConnectionAbortedError:
            return

        for i in range(LONG_TIME_EXPOSURE + 1):
            if self.app.app_state == "stop":
                return
            sleep(1)
            self.app.output.change_b(
                f"Under LONG exposure: {self.app.output.convert_seconds(i)}"
            )

        try:
            self.app.output.clear_all()
            self.app.output.change_a("Requesting end of exposure")
            sleep(0.3)
            self.app.com.end()
            self.app.output.change_a("Accepted end of exposure")
        except ConnectionAbortedError:
            return

        self.app.output.change_a(f"Exposure LONG Completed!")
        self.app.output.change_b(f"------------------------------")

    def end_exposure(self):
        sleep(1)
        try:
            self.app.output.clear_all()
            self.app.output.change_a("Requesting end of exposure")
            sleep(0.3)
            self.app.com.end()
            self.app.output.change_a("Accepted end of exposure")
        except ConnectionAbortedError:
            return

        self.app.output.change_a(f"Exposure CANCELLED")
        self.app.output.change_b(f"------------------------------")

    def start_smart_exposure(self) -> int:
        # for semi mode
        self.output.clear_all()
        total = 0
        try:
            total += self._wait_standby()
            self.app.com.start(variant="short")
            total += self._wait_exposure_start()
            total += self._wait_exposure_end()
            self.app.com.end()
        except RuntimeError:
            self.app.change_app_state("stop")
            self.output.exposure_aborted()
            return total
        self.output.exposure_success(total)
        self.app.change_app_state("stop")
        self.app.semi.action("stop")
        return total

    def start_smart_NO_exposure(self) -> int:
        # for semi mode
        self.output.clear_all()
        total = 0
        try:
            total += self._wait_calib_pass()
            self.app.com.end()
        except RuntimeError:
            self.app.change_app_state("stop")
            self.output.exposure_aborted()
            return total
        self.output.exposure_success(total)
        self.app.change_app_state("stop")
        self.app.semi.action("stop")
        return total

    def start_smart_loop(self) -> int:
        # for semi mode
        self.output.clear_all()
        total = 0
        exposures = 0
        while True:
            try:
                total += self._wait_standby(count=exposures)
                self.app.com.start(variant="short")
                total += self._wait_exposure_start()
                total += self._wait_exposure_end()
                self.app.com.end()
                exposures += 1
                if self._is_calib_passed():
                    break
            except RuntimeError:
                self.app.change_app_state("stop")
                self.output.exposure_aborted()
                break
        self.output.loop_success(exposures, total)
        self.app.change_app_state("stop")
        self.app.semi.action("stop")
        return total

    # AUTO MODE ----------------------------------
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
                    total = self.start_smart_NO_exposure()
                elif calibration in BASIC_CALIBRATIONS:
                    self.app.output.change_a(f"Starting {calibration} calib")
                    self.app.output.change_b(f"Stabilizing...")
                    sleep(2)
                    total += 2
                    self.app.mcu_interactor.click_calibration_button(calibration)
                    self.app.aws_interactor.enable_FPD_calib()
                total = self.start_smart_NO_exposure()
        except AttributeError:
            print("aborted")
            self.app.output.icon_not_found()
        except RuntimeError:
            print("aborted")
            self.app.output.calibration_aborted()
        else:
            print("Completed!")
            self.app.output.calibration_success(total)
