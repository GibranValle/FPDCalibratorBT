from Interaction.Interaction import Interaction
from typing import Literal


class MCU0(Interaction):
    mcu_clickable_tabs = Literal["calibration", "opt_calibration"]
    mu_clickable_tabs = Literal["calibration", "generator"]

    def __init__(self) -> None:
        super().__init__()

    def _check_calibration_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mcu_tabs("cal_selected")
        if x > 0 and y > 0:
            return True
        return False

    def _check_calibration_opt_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mcu_tabs("cal_opt_selected")
        if x > 0 and y > 0:
            return True
        return False

    def _check_mcu_page_1_or_calibration_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("cal_opt_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/2")
            # verify again
            if self._check_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("mcub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/2")
            # verify again
            if self._check_calibration_selected():
                return True
        return False

    def _check_mcu_page_1_or_calibration_opt_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("cal_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            # verify again
            if self._check_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("mcub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            # verify again
            if self._check_calibration_selected():
                return True
        return False

    def _check_mcu_page_0(self) -> bool:
        # if page 0 found, change to page 1
        x, y = self.cv.get_icon_coords_mcu_tabs("mcua")
        if x > 0 and y > 0:
            self.click_icon_mutl("only_right")
            return True
        return False

    def click_icon_mcu_tabs(self, button: mcu_clickable_tabs):
        if button == "calibration":
            if self._check_calibration_selected():
                return

            if self._check_mcu_page_1_or_calibration_unselected():
                return

            if self._check_mcu_page_0():
                if self._check_mcu_page_1_or_calibration_unselected():
                    return

            raise ValueError("Calibration tab not found")

        elif button == "opt_calibration":
            if self._check_calibration_opt_selected():
                return

            if self._check_mcu_page_1_or_calibration_opt_unselected():
                return

            if self._check_mcu_page_0():
                if self._check_mcu_page_1_or_calibration_opt_unselected():
                    return

            raise ValueError("Calibration Optional tab not found")
