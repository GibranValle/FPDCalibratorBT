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

    def click_ok(self):
        res = False
        if self._click_icon_aws("ok"):
            res = True
        if self._click_icon_aws("ok2"):
            res = True
        return res

    def enable_FPD_calib(self) -> bool:
        print("enabling")
        validation = True
        validation = self._click_icon_aws("calib")
        validation = self._click_icon_aws("calib")
        validation = self._click_icon_aws("field_calibration")
        if not validation:
            self.app.log("gui", "error", "FPD calibration not enabled")
            return False
        self.app.log("gui", "info", "FPD calibration enabled")
        return True

    def openRU(self) -> None:
        if self._process_exists("RuPcTool.exe"):
            self._changeWindow("RU PC-TOOL")
            return
        self._openApp("RuPcTool.exe")

    def closeRU(self):
        self.closeApp("RuPcTool.exe")

    def closeMUTL(self):
        self.closeApp("MUTL.exe")
