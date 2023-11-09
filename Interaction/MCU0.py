from Interaction.Interaction import Interaction
from typing import Literal
from ComputerVision.cv_types import mcu, mcu_opt, MCU, MCU_OPT


class MCU0(Interaction):
    from GUI.GUI import GUI

    mcu_clickable_tabs = Literal["calibration", "opt_calibration"]
    mu_clickable_tabs = Literal["calibration", "generator"]

    def __init__(self, app: GUI) -> None:
        super().__init__(app)

    def _open_MUTL_MCU(self) -> bool:
        if self._process_exists("MUTL.exe"):
            self._changeWindow("MCU0")
            self.app.log("mcu0", "info", "Program exists changing window")
            return True
        if self._openApp("MCU"):
            self.app.log("mcu0", "info", "Program not exists opening")
            return True
        self.app.log("mcu0", "error", "Program not installed")
        return False

    def _click_cal_opt_tab(self):
        # check if already selected
        x, y = self.cv.get_icon_coords("cal_opt_selected")
        if x > 0 and y > 0:
            self.app.log("mcu0", "info", "calibration opt already selected returning")
            print("calibration opt already selected returning")
            return True

        # check if page 1
        x, y, w, h = self.cv.get_icon_all_coords("mcub")
        if x > 0 and y > 0:
            self.app.log("mcu0", "info", "page 1 found, clicking cal opt tab")
            print("page 1 found, clicking cal opt tab")
            x, y = self._get_fraction_point(x, y, w, h, "3/4")
            self._click_point(x, y)
            return True

        # check if cal selected
        x, y, w, h = self.cv.get_icon_all_coords("cal_selected")
        if x > 0 and y > 0:
            self.app.log("mcu0", "info", "page 1 found, clicking cal opt tab")
            print("page 1 found, clicking cal opt tab")
            x, y = self._get_fraction_point(x, y, w, h, "3/4")
            print(x, y)
            self._click_point(x, y)
            return True

        # check if page 0
        x, y = self.cv.get_icon_coords("mcua")
        if x > 0 and y > 0:
            self.app.log("mcu0", "info", "page 0 found")
            print("page 0 found")
            x, y, w, h = self.cv.get_icon_all_coords("only_right")
            if x > 0 and y > 0:
                x, y = self._get_fraction_point(x, y, w, h, "3/4")
                self.app.log("mcu0", "info", "arrow found")
                print("arrow found... clicking")
                self._click_point(x, y)
                x, y, w, h = self.cv.get_icon_all_coords("mcub")
                if x > 0 and y > 0:
                    self.app.log("mcu0", "info", "page 1 found, clicking cal opt tab")
                    print("page 1 found, clicking cal opt tab")
                    x, y = self._get_fraction_point(x, y, w, h, "1/2")
                    self._click_point(x, y)
                    return True
        self.app.log("mcu0", "error", "Calibration opt tab not visible")
        print("Calibration opt tab not visible")
        return False

    def _click_cal_tab(self):
        # check if already selected
        x, y = self.cv.get_icon_coords("cal_selected")
        if x > 0 and y > 0:
            print("calibration already selected returning")
            return True

        # check if page 1
        x, y, w, h = self.cv.get_icon_all_coords("mcub")
        if x > 0 and y > 0:
            self.app.log("mcu0", "info", "page 1 found, clicking cal tab")
            print("page 1 found, clicking cal tab")
            x, y = self._get_fraction_point(x, y, w, h, "1/2")
            self._click_point(x, y)
            return True

        # check if calibration selected
        x, y, w, h = self.cv.get_icon_all_coords("cal_opt_selected")
        if x > 0 and y > 0:
            self.app.log("mcu0", "info", "page 1 found, clicking cal tab")
            print("page 1 found, clicking cal tab")
            x, y = self._get_fraction_point(x, y, w, h, "1/2")
            print(x, y)
            self._click_point(x, y)
            return True

        # check if page 0
        x, y = self.cv.get_icon_coords("mcua")
        if x > 0 and y > 0:
            self.app.log("mcu0", "info", "page 0 found")
            print("page 0 found")
            x, y, w, h = self.cv.get_icon_all_coords("only_right")
            if x > 0 and y > 0:
                x, y = self._get_fraction_point(x, y, w, h, "3/4")
                self.app.log("mcu0", "info", "arrow found")
                print("arrow found... clicking")
                self._click_point(x, y)
                x, y, w, h = self.cv.get_icon_all_coords("mcub")
                if x > 0 and y > 0:
                    self.app.log("mcu0", "info", "page 1 found, clicking cal tab")
                    print("page 1 found, clicking cal tab")
                    x, y = self._get_fraction_point(x, y, w, h, "1/2")
                    self._click_point(x, y)
                    return True
        self.app.log("mcu0", "error", "Calibration tab not visible")
        print("Cal tab not visible")
        return False

    def click_calibration_button(self, button: mcu | mcu_opt) -> None:
        online = not self.app.com.is_offline()
        try:
            if self._open_MUTL_MCU():
                self.app.output.clicked("MUTL")
            else:
                self.app.output.restart("MUTL")
                if online:
                    raise RuntimeError("MUTL not installed")
        except RuntimeError:
            return

        try:
            if button in MCU and self._click_cal_tab():
                self.app.output.clicked("Cal tab")
            elif button in MCU_OPT and self._click_cal_opt_tab():
                self.app.output.clicked("Cal Opt tab")
            else:
                self.app.output.restart("MUTL")
                if online:
                    raise RuntimeError("CAL OPT TAB NOT VISIBLE")
        except RuntimeError:
            return

        try:
            x, y = self.cv.get_icon_coords(button)
            if x > 0 and y > 0:
                self._click_point(x, y)
                self.app.output.clicked(f"{button}")
                return

            self.app.output.restart("MUTL")
            if online:
                raise RuntimeError(f"{button} button not visible")
        except RuntimeError:
            return
