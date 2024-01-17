from typing import Literal
from Interaction.Interaction import Interaction


class MU0(Interaction):
    from GUI.GUI import GUI

    mcu_clickable_tabs = Literal["calibration", "opt_calibration"]
    mu_clickable_tabs = Literal["calibration", "generator"]

    def __init__(self, app: GUI) -> None:
        super().__init__(app)
        self.app = app

    def _open_MUTL_MU(self) -> bool:
        if self._process_exists("MUTL.exe"):
            self._changeWindow("MU0")
            self.app.log("mu0", "info", "Program exists changing window")
            return True
        if self._openApp("MU"):
            self.app.log("mu0", "info", "Program not exists opening")
            return True
        self.app.log("mu0", "error", "Program not installed")
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

    def enable_ment(self) -> None:
        online = not self.app.com.is_offline()
        try:
            if self._open_MUTL_MU():
                self.app.output_log.append("MUTL opened")
            else:
                self.app.output_log.append("MUTL could not be opened, Retry")
                if online:
                    raise RuntimeError("MUTL not installed")
        except RuntimeError:
            return

        try:
            if self._click_generator_tab():
                self.app.output_log.append("Generator tab clicked")
            else:
                self.app.output_log.append("Generator tab could not be clicked")
                if online:
                    raise RuntimeError("GENERATOR TAB NOT VISIBLE")
        except RuntimeError:
            return

        try:
            x, y = self.cv.get_icon_coords("enable_ment")
            if x > 0 and y > 0:
                self._click_point(x, y)
                self.app.output_log.append("Enable ment mode clicked ")
                return
            self.app.output.restart("MUTL")
            self.app.output_log.append("MUTL could not be opened, Retry")
            if online:
                self.app.output_log.append("Enable ment mode button not visible")
                raise RuntimeError("Enable ment mode button not visible")
        except RuntimeError:
            return

    def toggle_MAG(self) -> None:
        online = not self.app.com.is_offline()
        try:
            if self._open_MUTL_MU():
                self.app.output_log.append("MUTL opened")
            else:
                self.app.output.restart("MUTL")
                if online:
                    self.app.output_log.append("MUTL not installed")
                    raise RuntimeError("MUTL not installed")
        except RuntimeError:
            return

        try:
            if self._click_calibration_tab():
                self.app.output.clicked("Calibration tab")
            else:
                self.app.output_log.append("MUTL could not be opened, Retry")
                if online:
                    self.app.output_log.append("GENERATOR TAB NOT VISIBLE")
                    raise RuntimeError("GENERATOR TAB NOT VISIBLE")
        except RuntimeError:
            return

        try:
            x, y = self.cv.get_icon_coords("MAG")
            if x > 0 and y > 0:
                self._click_point(x, y)                
                self.app.output_log.append("MAG clicked")
                return

            self.app.output.restart("MUTL")
            if online:
                self.app.output_log.append("MAG button not visible")
                raise RuntimeError("MAG button not visible")
        except RuntimeError:
            return

    def toggle_HVL(self) -> None:
        online = not self.app.com.is_offline()
        try:
            if self._open_MUTL_MU():
                self.app.output_log.append("MUTL opened")
            else:
                self.app.output_log.append("MUTL could not be opened, Retry")
                if online:
                    self.app.output_log.append("MUTL not installed")
                    raise RuntimeError("MUTL not installed")
        except RuntimeError:
            return

        try:
            if self._click_calibration_tab():
                self.app.output_log.append("Calibration tab clicked opened")
            else:
                self.app.output_log.append("MUTL could not be opened, Retry")
                if online:
                    self.app.output_log.append("Calibration tab not visible")
                    raise RuntimeError("Calibration tab not visible")
        except RuntimeError:
            return

        try:
            x, y = self.cv.get_icon_coords("HVL")
            if x > 0 and y > 0:
                self._click_point(x, y)
                self.app.output_log.append("HVL clicked")
                return

            self.app.output_log.append("MUTL could not be opened, Retry")
            if online:
                self.app.output_log.append("Calibration tab not visible")
                raise RuntimeError("Calibration tab not visible")
        except RuntimeError:
            return
