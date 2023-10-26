from types_interaction import fractions
from pyautogui import moveTo, click, position
from time import sleep
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import mutl, ru


class Interaction:
    def __init__(self) -> None:
        self.cv = ComputerVision()

    def _click_center(
        self,
        x: float,
        y: float,
        return2origin: bool = False,
    ):
        a: float = 0
        b: float = 0
        if return2origin:
            a, b = position()
        sleep(0.5)
        click(x, y)
        sleep(0.4)
        if return2origin:
            moveTo(a, b)

    def _click_fractions(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fraction: fractions,
        return2origin: bool = False,
    ):
        a: float = 0
        b: float = 0
        if return2origin:
            a, b = position()
        sleep(0.5)
        if fraction == "1/2":
            x0 = x + w / 2
            y0 = y + h / 2
            click(x0, y0)
        elif fraction == "1/4":
            x0 = x + w / 4
            y0 = y + h / 2
            click(x0, y0)
        elif fraction == "3/4":
            x0 = x + 3 * w / 4
            y0 = y + h / 2
            click(x0, y0)
        sleep(0.4)
        if return2origin:
            moveTo(a, b)

    def click_icon_mutl(self, button: mutl):
        x, y = self.cv.get_icon_coords_mutl(button)
        if x > 0 and y > 0:
            self._click_center(x, y, True)

    def click_icon_ru(self, button: ru):
        x, y = self.cv.get_icon_coords_ru(button)
        if x > 0 and y > 0:
            self._click_center(x, y, True)
