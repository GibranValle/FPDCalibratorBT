from Interaction.Interaction import Interaction
from ComputerVision.cv_types import aws, gen


class AWSGen(Interaction):
    def __init__(self) -> None:
        super().__init__()

    def click_icon_aws(self, button: aws):
        x, y = self.cv.get_icon_coords_aws(button)
        if x > 0 and y > 0:
            self._click_center(x, y, True)

    def click_icon_gen(self, button: gen):
        x, y = self.cv.get_icon_coords_gen(button)
        if x > 0 and y > 0:
            self._click_center(x, y, True)
