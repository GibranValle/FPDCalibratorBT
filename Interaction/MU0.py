from typing import Literal
from Interaction.Interaction import Interaction
from ComputerVision.cv_types import mu, mu_gen


class MU0(Interaction):
    mcu_clickable_tabs = Literal["calibration", "opt_calibration"]
    mu_clickable_tabs = Literal["calibration", "generator"]

    def __init__(self) -> None:
        super().__init__()

    def _check_mu_calibration_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mu_tabs("calibration_selected")
        if x > 0 and y > 0:
            return True
        return False

    def _check_generator_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mu_tabs("generator_selected")
        if x > 0 and y > 0:
            return True
        return False

    def _check_mu_page_0(self) -> bool:
        # if page 0 found, change to page 1
        x, y = self.cv.get_icon_coords_mu_tabs("mua")
        if x > 0 and y > 0:
            x, y = self.cv.get_icon_coords_mutl("only_right")
            self._click_center(x, y)
            return True
        return False

    def _check_mu_page_1_or_calibration_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mu_tabs("generator_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/4")
            # verify again
            if self._check_mu_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mu_tabs("mub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/4")
            # verify again
            if self._check_mu_calibration_selected():
                return True
        return False

    def _check_mu_page_1_or_generator_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("cal_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            # verify again
            if self._check_mu_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("mcub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            # verify again
            if self._check_mu_calibration_selected():
                return True
        return False

    def click_mu_icon(self, button: mu):
        x, y = self.cv.get_icon_coords_mu(button)
        if x > 0 and y > 0:
            return True
        return False

    def click_mu_gen_icon(self, button: mu_gen):
        x, y = self.cv.get_icon_coords_mu_gen(button)
        if x > 0 and y > 0:
            return True
        return False

    def click_icon_mu_tabs(self, button: mu_clickable_tabs):
        if button == "calibration":
            if self._check_mu_calibration_selected():
                return

            if self._check_mu_page_1_or_calibration_unselected():
                if self._check_mu_calibration_selected():
                    return

            if self._check_mu_page_0():
                if self._check_mu_page_1_or_calibration_unselected():
                    if self._check_mu_calibration_selected():
                        return

            raise ValueError("Calibration tab not found")

        elif button == "generator":
            if self._check_generator_selected():
                return

            if self._check_mu_page_1_or_generator_unselected():
                if self._check_generator_selected():
                    return

            if self._check_mu_page_0():
                if self._check_mu_page_1_or_generator_unselected():
                    if self._check_generator_selected():
                        return

            raise ValueError("Generator tab not found")
