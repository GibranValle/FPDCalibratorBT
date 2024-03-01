from typing import Literal
from Interaction.Interaction import Interaction


class MU0(Interaction):
    from GUI.GUI import GUI

    mcu_clickable_tabs = Literal["calibration", "opt_calibration"]
    mu_clickable_tabs = Literal["calibration", "generator"]

    def __init__(self, app: GUI) -> None:
        super().__init__(app)
        self.app = app

    def open_MUTL_MU(self) -> bool:
        if self._process_exists("MUTL.exe"):
            self._changeWindow("MU0")
            self.app.file_log("mu0", "info", "Program exists changing window")
            return True
        if self._openApp("MU"):
            self.app.file_log("mu0", "error", "RUPCTools not installed")
            return True
        self.app.window_log("Error: RU not installed")
        self.app.file_log("mcu0", "error", "RUPCTools not installed")
        return False

    def _click_generator_tab(self):
        # check if already selected
        x, y = self.cv.get_icon_coords("generator_selected")
        if x > 0 and y > 0:
            print("generator already selected returning")
            return True

        # check if page 1
        x, y, w, h = self.cv.get_icon_all_coords("mub")
        if x > 0 and y > 0:
            print("page 1 found, clicking generator tab")
            x, y = self._get_fraction_point(x, y, w, h, "1/2")
            self._click_point(x, y)
            return True

        # check if calibration selected
        x, y, w, h = self.cv.get_icon_all_coords("calibration_selected")
        if x > 0 and y > 0:
            print("page 1 found, clicking generator tab")
            x, y = self._get_fraction_point(x, y, w, h, "1/2")
            print(x, y)
            self._click_point(x, y)
            return True

        # check if page 0
        x, y = self.cv.get_icon_coords("mua")
        if x > 0 and y > 0:
            print("page 0 found")
            x, y, w, h = self.cv.get_icon_all_coords("only_right")
            if x > 0 and y > 0:
                x, y = self._get_fraction_point(x, y, w, h, "3/4")
                print("arrow found... clicking")
                self._click_point(x, y)
                x, y, w, h = self.cv.get_icon_all_coords("mub")
                if x > 0 and y > 0:
                    print("page 1 found, clicking generator tab")
                    x, y = self._get_fraction_point(x, y, w, h, "1/2")
                    self._click_point(x, y)
                    return True
        print("Generator tab not visible")
        return False

    def _click_calibration_tab(self):
        # check if already selected
        x, y = self.cv.get_icon_coords("calibration_selected")
        if x > 0 and y > 0:
            print("calibration already selected returning")
            return True

        # check if page 1
        x, y, w, h = self.cv.get_icon_all_coords("mub")
        if x > 0 and y > 0:
            print("page 1 found, clicking generator tab")
            x, y = self._get_fraction_point(x, y, w, h, "1/4")
            self._click_point(x, y)
            return True

        # check if calibration selected
        x, y, w, h = self.cv.get_icon_all_coords("generator_selected")
        if x > 0 and y > 0:
            print("page 1 found, clicking calibration tab")
            x, y = self._get_fraction_point(x, y, w, h, "1/4")
            print(x, y)
            self._click_point(x, y)
            return True

        # check if page 0
        x, y = self.cv.get_icon_coords("mua")
        if x > 0 and y > 0:
            print("page 0 found")
            x, y, w, h = self.cv.get_icon_all_coords("only_right")
            if x > 0 and y > 0:
                x, y = self._get_fraction_point(x, y, w, h, "3/4")
                print("arrow found... clicking")
                self._click_point(x, y)
                x, y, w, h = self.cv.get_icon_all_coords("mub")
                if x > 0 and y > 0:
                    print("page 1 found, clicking calibration tab")
                    x, y = self._get_fraction_point(x, y, w, h, "1/4")
                    self._click_point(x, y)
                    return True
        print("Calibration tab not visible")
        return False

    def enable_ment_mode(self) -> bool:
        online = not self.app.com.is_offline()
        try:
            if self.open_MUTL_MU():
                self.app.window_log("MUTL opened")
            else:
                self.app.window_log("MUTL could not be opened, Retry")
                if online:
                    raise RuntimeError("MUTL not installed")
        except RuntimeError:
            return False

        try:
            if self._click_generator_tab():
                self.app.window_log("Generator tab clicked")
            else:
                self.app.window_log("Generator tab could not be clicked")
                if online:
                    raise RuntimeError("GENERATOR TAB NOT VISIBLE")
        except RuntimeError:
            return False

        try:
            x, y = self.cv.get_icon_coords("enable_ment")
            if x > 0 and y > 0:
                self._click_point(x, y)
                self.app.window_log("Enable ment mode clicked ")
                return True
            self.app.window_log("MUTL could not be opened, Retry")
            if online:
                self.app.window_log("Enable ment mode button not visible")
                raise RuntimeError("Enable ment mode button not visible")
        except RuntimeError:
            return False
        return True

    def toggle_MAG(self) -> bool:
        online = not self.app.com.is_offline()
        try:
            if self.open_MUTL_MU():
                self.app.window_log("MUTL opened")
            else:
                if online:
                    self.app.window_log("MUTL not installed")
                    raise RuntimeError("MUTL not installed")
        except RuntimeError:
            return False

        try:
            if self._click_calibration_tab():
                self.app.window_log("Calibration tab clicked")
            else:
                self.app.window_log("MUTL could not be opened, Retry")
                if online:
                    self.app.window_log("GENERATOR TAB NOT VISIBLE")
                    raise RuntimeError("GENERATOR TAB NOT VISIBLE")
        except RuntimeError:
            return False

        try:
            x, y = self.cv.get_icon_coords("MAG")
            if x > 0 and y > 0:
                self._click_point(x, y)
                self.app.window_log("MAG clicked")
                return True

            if online:
                self.app.window_log("MAG button not visible")
                raise RuntimeError("MAG button not visible")
        except RuntimeError:
            return False

        return True

    def toggle_HVL(self) -> bool:
        online = not self.app.com.is_offline()
        try:
            if self.open_MUTL_MU():
                self.app.window_log("MUTL opened")
            else:
                self.app.window_log("MUTL could not be opened, Retry")
                if online:
                    self.app.window_log("MUTL not installed")
                    raise RuntimeError("MUTL not installed")
        except RuntimeError:
            return False

        try:
            if self._click_calibration_tab():
                self.app.window_log("Calibration tab clicked")
            else:
                self.app.window_log("MUTL could not be opened, Retry")
                if online:
                    self.app.window_log("Calibration tab not visible")
                    raise RuntimeError("Calibration tab not visible")
        except RuntimeError:
            return False

        try:
            x, y = self.cv.get_icon_coords("HVL")
            if x > 0 and y > 0:
                self._click_point(x, y)
                self.app.window_log("HVL clicked")
                return True

            self.app.window_log("MUTL could not be opened, Retry")
            if online:
                self.app.window_log("Calibration tab not visible")
                raise RuntimeError("Calibration tab not visible")
        except RuntimeError:
            return False

        return True
