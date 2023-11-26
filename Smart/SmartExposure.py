from ComputerVision.cv_types import status_gen, status_mu, status_mcu
from time import sleep
from Smart.constants import *
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import status_mcu


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
        x, y = self.cv.get_icon_coords(button)
        if x > 0 and y > 0:
            self.status_gen = button
        else:
            self.status_gen = "idle"

    def _get_mu_state(self, button: status_mu) -> None:
        x, y = self.cv.get_icon_coords(button)
        if x > 0 and y > 0:
            self.status_mu = button
        else:
            self.status_mu = "offline"

    def _get_mcu_state(self, button: status_mcu) -> None:
        x, y = self.cv.get_icon_coords(button)
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
            print(self.status_mcu)
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
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
            elif self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            total += i
        return total

    def _wait_standby(self, exposure: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_STANDBY):
            sleep(SLEEP_TIME)
            self._get_mu_state("standby")
            self._get_gen_state("push")
            self.output.waiting_ready(i)
            if exposure > 0 and self._is_calib_passed():
                return i
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "push" or self.status_mu == "standby":
                self.log(
                    "smart", "info", f"xray gen is ready for exposure, waited: {i}"
                )
                break
            total += i
        return total

    def _wait_exposure_start(self, exposure: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_BEFORE_EXPOSURE):
            sleep(SLEEP_TIME)
            self._get_mu_state("exposure")
            self._get_gen_state("exposing")
            self.output.waiting_exposure_start(i)
            if exposure > 0 and self._is_calib_passed():
                return i
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "exposing" or self.status_mu == "exposure":
                self.log("smart", "info", f"xray gen should be exposing, waited: {i}")
                break
            total += i
        return total

    def _wait_exposure_end(self, exposure: int = 0) -> int:
        total = 0
        for i in range(MAX_TIME_EXPOSURE):
            sleep(SLEEP_TIME)
            self._get_mu_state("blocked")
            self._get_gen_state("release")
            self.output.waiting_exposure_end(i)
            if exposure > 0 and self._is_calib_passed():
                return i
            if self.app.app_state == "pause":
                self.output.in_pause(i)
                continue
            elif self.app.app_state == "stop":
                self.output.exposure_aborted()
                self.log("smart", "error", "request of abortion")
                raise RuntimeError("Aborted requested")
            elif self.status_gen == "release" or self.status_mu == "blocked":
                self.log("smart", "info", f"end of exposure, waited: {i}")
                break
            total += i
        return total

    def _is_calib_passed(self) -> bool:
        self._get_mcu_state("pasar")
        self._get_mcu_state("saltar")
        if self.status_mcu == "pasar" or self.status_mcu == "saltar":
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

    def start_smart_exposure(self):
        self.output.clear_all()
        total = 0
        try:
            total += self._wait_standby()
            total += self._wait_exposure_start()
            total += self._wait_exposure_end()
        except RuntimeError:
            self.app.change_app_state("stop")
            self.output.exposure_aborted()
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
                total += self._wait_standby(exposures)
                if self._is_calib_passed():
                    break
            except RuntimeError:
                self.output.exposure_aborted()
                break

            try:
                self.app.com.communicate("L")
            except ConnectionError:
                self.output.exposure_abnormal()
                return

            try:
                total += self._wait_exposure_start(exposures)
                if self._is_calib_passed():
                    break
            except RuntimeError:
                self.output.exposure_aborted()
                break

            try:
                total += self._wait_exposure_end(exposures)
                if self._is_calib_passed():
                    break
                exposures += 1
            except RuntimeError:
                self.output.exposure_aborted()
                break
        self.app.change_app_state("stop")

    def auto_loop(self, calibration: status_mcu):
        online = not self.app.com.is_offline()
        print("auto loop")
        self.output.clear_all()
        total = 0
        try:
            total += self._wait_calib_start(calibration)
        except RuntimeError:
            print("calib start not found")
            if online:
                raise RuntimeError("aborted")

        try:
            total += self._wait_calib_end()
        except RuntimeError:
            print("exposure signal end not found")
            if online:
                raise RuntimeError("aborted")
        self.app.change_app_state("stop")
        return total

    def auto_loop_exposure(self, calibration: status_mcu):
        print("auto loop")
        self.output.clear_all()
        total = 0
        exposures = 0
        while True:
            try:
                total += self._wait_calib_start(calibration, exposures)
                if self._is_calib_passed():
                    break
            except RuntimeError:
                print("calib start not found")
                raise RuntimeError("aborted")

            try:
                total += self._wait_standby(exposures)
                if self._is_calib_passed():
                    break
            except RuntimeError:
                print("standby signal not found")
                raise RuntimeError("aborted")
            
            try:
                self.app.com.communicate("S")
            except ConnectionError:
                self.output.exposure_abnormal()
                return

            try:
                total += self._wait_exposure_start(exposures)
                if self._is_calib_passed():
                    break
            except RuntimeError:
                print("exposure signal not found")
                raise RuntimeError("aborted")
            
            try:
                self.app.com.communicate("X")
            except ConnectionError:
                self.output.exposure_abnormal()
                return

            try:
                total += self._wait_exposure_end(exposures)
                if self._is_calib_passed():
                    break
                exposures += 1
            except RuntimeError:
                print("exposure signal end not found")
                raise RuntimeError("aborted")

        self.app.change_app_state("stop")
        return total

    def start_auto_loop(self):
        total = 0
        new_calib: status_mcu = "offline"
        try:
            for calibration in self.app.selected_cal:
                if calibration == "offset" or calibration == "defect":
                    self.app.output.change_a(f"Starting {calibration} calib")
                    self.app.output.change_b(f"Stabilizing...")
                    sleep(2)
                    total += 2
                    self.app.output.change_b(f"No exposure required")
                    self.app.mcu_interactor.click_calibration_button(calibration)
                    self.app.aws_interactor.enable_FPD_calib()
                    try:
                        if calibration == "offset":
                            new_calib = "offset"
                        elif calibration == "defect":
                            new_calib = "defect_solid"
                        total += self.auto_loop(new_calib)
                    except RuntimeError:
                        raise RuntimeError
        except RuntimeError:
            print("aborted")
            self.app.output.calibration_aborted()
        else:
            print("Completed!")
            self.app.output.calibration_success(total)
