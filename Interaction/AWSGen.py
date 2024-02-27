from Interaction.Interaction import Interaction
from ComputerVision.cv_types import aws, gen
from time import sleep


class AWSGen(Interaction):
    from GUI.GUI import GUI

    def __init__(self, app: GUI) -> None:
        super().__init__(app)

    def _click_icon_aws(self, button: aws) -> bool:
        x, y = self.cv.get_icon_coords(button)
        if x > 0 and y > 0:
            if button == "calib":
                self._click_point(x, y, False)
                sleep(0.3)
                self._click_point(x, y, False)
            else:
                self._click_point(x, y, True)
            return True
        return False

    def _click_icon_gen(self, button: gen) -> bool:
        x, y = self.cv.get_icon_coords(button)
        if x > 0 and y > 0:
            self._click_point(x, y, True)
            return True
        return False

    def click_ok(self) -> bool:
        validation = self._click_icon_aws("ok")
        if not validation:
            return validation
        self.app.log("gui", "info", "AWS ok button pushed")
        self.app.output_log.append("AWS ok button pushed")
        return validation

    def click_calib_button(self) -> bool:
        validation = self._click_icon_aws("calib")
        if not validation:
            print("AWS calib button not pushed")
            self.app.output_log.append("AWS calib button not pushed")
            self.app.log("gui", "error", "AWS calib button not pushed")
            return validation
        self.app.log("gui", "info", "AWS calib button pushed")
        self.app.output_log.append("AWS calib button pushed")
        return validation

    def click_field_button(self) -> bool:
        validation = self._click_icon_aws("field_calibration")
        if not validation:
            self.app.output_log.append("AWS field calib button not pushed")
            self.app.log("gui", "error", "AWS field calib button not pushed")
            return validation
        self.app.log("gui", "info", "AWS field calib button pushed")
        self.app.output_log.append("AWS field calib button pushed")
        return validation

    def enable_FPD_calib(self) -> bool:
        validation = self.click_calib_button()
        validation = validation and self.click_field_button()
        if not validation:
            self.app.log("gui", "error", "FPD calibration not enabled")
            return validation
        self.app.log("gui", "info", "FPD calibration enabled")
        return validation

    def openRU(self) -> None:
        if self._process_exists("RuPcTool.exe"):
            self._changeWindow("RU PC-TOOL")
            return
        self._openApp("RuPcTool.exe")

    def openFF_Gen(self) -> bool:
        if self._process_exists("FF_Generator_Tool_v1_00_10.exe"):
            self._changeWindow("FF_Generator_Tool")
            return True
        if self._openApp("FF_Generator_Tool_v1_00_10.exe"):
            self.app.log("mcu0", "error", "RUPCTools not installed")
            return True
        self.app.output_log.append("Error: FF_Generator_Tool\nnot installed")
        self.app.log("mcu0", "error", "FF_Generator_Tool not installed")
        return False

    def closeRU(self):
        self.closeApp("RuPcTool.exe")

    def closeMUTL(self):
        self.closeApp("MUTL.exe")
