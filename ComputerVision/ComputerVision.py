from pyautogui import locateCenterOnScreen, locateOnScreen
from typing import Literal
from ComputerVision.image_repository import *
from ComputerVision.cv_types import *

fraction = Literal["1/4", "1/2", "3/4"]


class ComputerVision:
    def __init__(self):
        self.image_repository = image_repository

    def get_status(
        self, button: status_gen | status_mcu | status_mu
    ) -> tuple[int, int]:
        dir: keys = "status_gen"
        confidence = 0.95

        if button in STATUS_GEN:
            dir: keys = "status_gen"
        elif button in STATUS_MCU:
            dir: keys = "status_mcu"
        elif button in STATUS_MU:
            dir: keys = "status_mu"
        try:
            path: str = self.image_repository[dir][button]
            x, y = locateCenterOnScreen(path, confidence=confidence)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords(self, button: all_buttons) -> tuple[int, int]:
        dir: keys = "aws"
        if button in AWS:
            dir: keys = "aws"
        elif button in GEN:
            dir: keys = "gen"
        elif button in MCU:
            dir: keys = "mcu"
        elif button in MCU_OPT:
            dir: keys = "mcu_opt"
        elif button in MCU_TABS:
            dir: keys = "mcu_tabs"
        elif button in MCU_OPT:
            dir: keys = "mcu_opt"
        if button in MU:
            dir: keys = "mu"
        elif button in MUTL:
            dir: keys = "mutl"
        elif button in MU_GEN:
            dir: keys = "mu_gen"
        elif button in MU_TABS:
            dir: keys = "mu_tabs"
        elif button in RU:
            dir: keys = "ru"
        path: str = self.image_repository[dir][button]
        try:
            confidence = 0.95
            x, y = locateCenterOnScreen(path, confidence=confidence)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_all_coords(
        self, button: mcu_tabs | mu_tabs | mutl
    ) -> tuple[int, int, int, int]:
        dir: keys = "mu_tabs"
        if button in MCU_TABS:
            dir: keys = "mcu_tabs"
        elif button in MUTL:
            dir: keys = "mutl"
        path: str = self.image_repository[dir][button]
        try:
            x, y, w, h = locateOnScreen(path)  # type: ignore
            return x, y, w, h  # type: ignore
        except TypeError:
            return -1, -1, -1, -1

    @DeprecationWarning
    def _get_status(self, name: str):
        for key, folder in self.image_repository.items():
            if name in key:
                for status, path in folder.items():
                    try:
                        x, y = locateCenterOnScreen(path, confidence=0.85)  # type: ignore
                        setattr(self, f"{name}", status)
                    except TypeError:
                        pass
        return getattr(self, f"{name}")
