from typing import Literal
from Interaction.Interaction import Interaction
from ComputerVision.cv_types import mu, mu_gen


class MU0(Interaction):
    from GUI.GUI import GUI

    mcu_clickable_tabs = Literal["calibration", "opt_calibration"]
    mu_clickable_tabs = Literal["calibration", "generator"]

    def __init__(self, app: GUI) -> None:
        super().__init__(app)
        self.app = app

    # -------- INTERNALS -------------------------------
    def _check_mu_calibration_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mu_tabs("calibration_selected")
        if x > 0 and y > 0:
            self.app.log("gui", "info", "Calibration tab already selected")
            return True
        self.app.log("gui", "error", "Calibration tab not selected")
        return False

    def _check_generator_selected(self) -> bool:
        # if tab already selected return
        x, y = self.cv.get_icon_coords_mu_tabs("generator_selected")
        if x > 0 and y > 0:
            self.app.log("gui", "info", "Generator tab already selected")
            return True
        self.app.log("gui", "error", "Generator tab not selected")
        return False

    def _check_mu_page_0(self) -> bool:
        # if page 0 found, change to page 1
        x, y = self.cv.get_icon_coords_mu_tabs("mua")
        if x > 0 and y > 0:
            x, y = self.cv.get_icon_coords_mutl("only_right")
            self._click_center(x, y)
            self.app.log("gui", "info", "MU Page 0 found")
            return True
        self.app.log("gui", "error", "MU Page 0 not found")
        return False

    def _check_mu_page_1_or_calibration_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mu_tabs("generator_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/4")
            self.app.log("gui", "info", "MU Page 1 found")
            # verify again
            if self._check_mu_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mu_tabs("mub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "1/4")
            self.app.log("gui", "info", "MU Page 1 found")
            # verify again
            if self._check_mu_calibration_selected():
                return True
        return False

    def _check_mu_page_1_or_generator_unselected(self) -> bool:
        # if page 1 or unselected found, click tab
        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("cal_selected")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            self.app.log("gui", "info", "MU Page 1 found")
            # verify again
            if self._check_mu_calibration_selected():
                return True

        x, y, w, h = self.cv.get_icon_all_coords_mcu_tabs("mcub")
        if x > 0 and y > 0:
            self._click_fractions(x, y, w, h, "3/4")
            self.app.log("gui", "info", "MU Page 1 found")
            # verify again
            if self._check_mu_calibration_selected():
                return True
        return False

    def _click_mu_icon(self, button: mu):
        x, y = self.cv.get_icon_coords_mu(button)
        if x > 0 and y > 0:
            return True
        self.app.log("gui", "error", "MU icon not found")
        raise ValueError("icon not found")

    def _click_mu_gen_icon(self, button: mu_gen):
        x, y = self.cv.get_icon_coords_mu_gen(button)
        if x > 0 and y > 0:
            return True
        self.app.log("gui", "error", "GEN icon not found")
        raise ValueError("icon not found")

    def _open_MUTL_MU(self) -> None:
        print("_open_mutl_mu")
        if self._process_exists("MUTL.exe"):
            print("MUTL exists...")
            self._changeWindow("MU0")
            self.app.log("gui", "info", "Program exists changing window")
            return
        if self._openApp("MU"):
            print("MUTL not exists but opened...")
            return
        raise AttributeError("Program not installed")

    def _click_icon_mu_tabs(self, button: mu_clickable_tabs) -> None:
        """Raise exception if not found"""
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

            self.app.log("gui", "error", "Tab not found")
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

            self.app.log("gui", "error", "Tab not found")
            raise ValueError("Generator tab not found")

    # -------- INTERNALS -------------------------------

    # ------------------- EXPORT ------------------------
    def enable_ment(self) -> None:
        try:
            print("opening RU MUTL MU mcu")
            self._open_MUTL_MU()
        except AttributeError:
            print("Program not installed")
            if not self.app.com.is_offline():
                self.app.output.restart()
                print("RU not install")
            print("offline mode continuing")
        try:
            self._click_icon_mu_tabs("generator")
            print("generator tab selected")
            self._click_mu_gen_icon("enable_ment")
            print("enable ment mode selected")
        except ValueError:
            if not self.app.com.is_offline():
                self.app.output.restart()
                print("ERROR")
            print("Enable mode not found")

    def toggle_MAG(self) -> None:
        try:
            self._open_MUTL_MU()
            self._click_icon_mu_tabs("calibration")
            self._click_mu_icon("MAG")
        except ValueError:
            if not self.app.com.is_offline():
                self.app.output.restart()
                print("ERROR")

    def toggle_HVL(self) -> None:
        try:
            self._open_MUTL_MU()
            self._click_icon_mu_tabs("calibration")
            self._click_mu_icon("HVL")
        except ValueError:
            if not self.app.com.is_offline():
                self.app.output.restart()
                print("ERROR")

    # ------------------- EXPORT ------------------------
