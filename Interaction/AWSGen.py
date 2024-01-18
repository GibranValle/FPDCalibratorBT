from Interaction.Interaction import Interaction
from ComputerVision.cv_types import aws, gen


class AWSGen(Interaction):
    from GUI.GUI import GUI

    def __init__(self, app: GUI) -> None:
        super().__init__(app)

    def _click_icon_aws(self, button: aws):
        x, y = self.cv.get_icon_coords(button)
        if x > 0 and y > 0:
            self._click_point(x, y, True)
            return
        return False

    def _click_icon_gen(self, button: gen):
        x, y = self.cv.get_icon_coords(button)
        if x > 0 and y > 0:
            self._click_point(x, y, True)
            return
        return False

    def enable_FPD_calib(self):
        validation = True
        validation = self._click_icon_aws("calib")
        validation = self._click_icon_aws("calib")
        if not validation:
            print("AWS calib button not pushed")
            self.app.output_log.append("AWS calib button not pushed")
            self.app.log("gui", "error", "AWS calib button not pushed")
            return validation
        self.app.log("gui", "info", "AWS calib button pushed")
        self.app.output_log.append("AWS calib button pushed")
        return validation
    
    def click_calib_button(self):
        validation = True
        validation = self._click_icon_aws("calib")
        validation = self._click_icon_aws("calib")
        if not validation:
            print("AWS calib button not pushed")
            self.app.output_log.append("AWS calib button not pushed")
            self.app.log("gui", "error", "AWS calib button not pushed")
            return validation
        self.app.log("gui", "info", "AWS calib button pushed")
        self.app.output_log.append("AWS calib button pushed")
        return validation
    

    def click_field_button(self):
        validation = True
        validation = self._click_icon_aws("field_calibration")
        if not validation:
            self.app.output_log.append("AWS field calib button not pushed")
            self.app.log("gui", "error", "AWS field calib button not pushed")
            return validation
        self.app.log("gui", "info", "AWS field calib button pushed")
        self.app.output_log.append("AWS field calib button not pushed")
        return validation
    
    def enable_FPD_calib(self):
        validation = True
        validation = self.click_calib_button()
        validation = self.click_field_button()        
        if not validation:
            self.app.log("gui", "error", "FPD calibration not enabled")
        self.app.log("gui", "info", "FPD calibration enabled")

    def openRU(self) -> None:
        if self._process_exists("RuPcTool.exe"):
            self._changeWindow("RU PC-TOOL")
            return
        self._openApp("RuPcTool.exe")

    def closeRU(self):
        self.closeApp("RuPcTool.exe")

    def closeMUTL(self):
        self.closeApp("MUTL.exe")
