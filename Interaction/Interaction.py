from types_interaction import fractions
from pyautogui import moveTo, click, position
from time import sleep


class Interaction:
    def __init__(self) -> None:
        pass

    def click_button(
        self, x: float, y: float, fraction: fractions, return2origin: bool = False
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
