from Interaction.Interaction import Interaction
from typing import Literal
from ComputerVision.cv_types import mcu, mcu_opt


class MCU0(Interaction):
    from GUI.GUI import GUI

    mcu_clickable_tabs = Literal["calibration", "opt_calibration"]
    mu_clickable_tabs = Literal["calibration", "generator"]

    def __init__(self, app: GUI) -> None:
        super().__init__(app)

    # -------- INTERNALS -------------------------------
    def _check_calibration_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mcu_tabs("cal_selected")
        if x > 0 and y > 0:
            return True
        self.app.log("gui", "error", "Calibration tab not selected")
        return False

    def _check_calibration_opt_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mcu_tabs("cal_opt_selected")
        if x > 0 and y > 0:
            return True
        self.app.log("gui", "error", "Calibration opt tab not selected")
        return False

    def _check_mcu_page_1_or_calibration_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("cal_opt_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/2")
            self.app.log("gui", "info", "MCU PAGE 1 FOUND")
            # verify again
            if self._check_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("mcub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/2")
            self.app.log("gui", "info", "MCU PAGE 1 FOUND")
            # verify again
            if self._check_calibration_selected():
                return True
        self.app.log("gui", "error", "MCU PAGE 1 not FOUND")
        return False

    def _check_mcu_page_1_or_calibration_opt_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("cal_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            self.app.log("gui", "info", "MCU PAGE 1 FOUND")
            # verify again
            if self._check_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("mcub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            self.app.log("gui", "info", "MCU PAGE 1 FOUND")
            # verify again
            if self._check_calibration_selected():
                return True
        self.app.log("gui", "error", "MCU PAGE 1 not FOUND")
        return False

    def _check_mcu_page_0(self) -> bool:
        # if page 0 found, change to page 1
        x, y = self.cv.get_icon_coords_mcu_tabs("mcua")
        if x > 0 and y > 0:
            self._click_icon_mutl("only_right")
            return True
        self.app.log("gui", "error", "MCU PAGE 0 not FOUND")
        return False

    def _click_icon_mcu_tabs(self, button: mcu_clickable_tabs):
        if button == "calibration":
            if self._check_calibration_selected():
                return

            if self._check_mcu_page_1_or_calibration_unselected():
                return

            if self._check_mcu_page_0():
                if self._check_mcu_page_1_or_calibration_unselected():
                    return
            self.app.log("gui", "error", "MCU tab not FOUND")
            raise ValueError("Calibration tab not found")

        elif button == "opt_calibration":
            if self._check_calibration_opt_selected():
                return

            if self._check_mcu_page_1_or_calibration_opt_unselected():
                return

            if self._check_mcu_page_0():
                if self._check_mcu_page_1_or_calibration_opt_unselected():
                    return

            self.app.log("gui", "error", "MCU tab not FOUND")
            raise ValueError("Calibration Optional tab not found")

    # -------- INTERNALS -------------------------------

    # -------- EXPORT -------------------------------
    def click_mcu_calibration(self, button: mcu):
        try:
            self._click_icon_mcu_tabs("calibration")
            x, y = self.cv.get_icon_coords_mcu(button)
            if x > 0 and y > 0:
                self._click_center(x, y)
                return
            self.app.log("gui", "error", f"{button} not found")
            self.app.output.restart()
            print("ERROR")
        except ValueError:
            if not self.app.com.is_offline():
                self.app.output.restart()
                print("ERROR")

    def click_mcu_opt_calibration(self, button: mcu_opt):
        try:
            self._click_icon_mcu_tabs("calibration")
            x, y = self.cv.get_icon_coords_mcu_opt(button)
            if x > 0 and y > 0:
                self._click_center(x, y)
                return
            self.app.log("gui", "error", f"{button} not found")
            self.app.output.restart()
            print("ERROR")
        except ValueError:
            if not self.app.com.is_offline():
                self.app.output.restart()
                print("ERROR")
