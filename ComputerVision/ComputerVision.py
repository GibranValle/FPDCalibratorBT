from pyautogui import locateCenterOnScreen, locateOnScreen
from typing import Literal
from ComputerVision.image_repository import *
from ComputerVision.cv_types import *

fraction = Literal["1/4", "1/2", "3/4"]


class ComputerVision:
    def __init__(self):
        self.status_mu: status_mu = "offline"
        self.status_mcu: status_mcu = "offline"
        self.status_gen: status_gen = "idle"
        self.image_repository = image_repository

    def get_icon_coords_status_gen(self, button: status_gen) -> tuple[float, float]:
        dir: keys = "status_gen"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_status_mu(self, button: status_mu) -> tuple[float, float]:
        dir: keys = "status_mu"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_status_mcu(self, button: status_mcu) -> tuple[float, float]:
        dir: keys = "status_mcu"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_aws(self, button: aws) -> tuple[float, float]:
        dir: keys = "aws"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_gen(self, button: gen) -> tuple[float, float]:
        dir: keys = "gen"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_mcu(self, button: mcu) -> tuple[float, float]:
        dir: keys = "mcu"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_mcu_opt(self, button: mcu_opt) -> tuple[float, float]:
        dir: keys = "mcu_opt"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_mcu_tabs(self, button: mcu_tabs) -> tuple[float, float]:
        dir: keys = "mcu_tabs"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_all_coords_mcu_tabs(
        self, button: mcu_tabs
    ) -> tuple[float, float, float, float]:
        dir: keys = "mcu_tabs"
        path: str = self.image_repository[dir][button]
        try:
            x, y, w, h = locateOnScreen(path)  # type: ignore
            return x, y, w, h  # type: ignore
        except TypeError:
            return -1, -1, -1, -1

    def get_icon_coords_mu(self, button: mu) -> tuple[float, float]:
        dir: keys = "mu"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_mu_gen(self, button: mu_gen) -> tuple[float, float]:
        dir: keys = "mu"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_mu_tabs(self, button: mu_tabs) -> tuple[float, float]:
        dir: keys = "mu_tabs"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_all_coords_mu_tabs(
        self, button: mu_tabs
    ) -> tuple[float, float, float, float]:
        dir: keys = "mu_tabs"
        path: str = self.image_repository[dir][button]
        try:
            x, y, w, h = locateOnScreen(path)  # type: ignore
            return x, y, w, h  # type: ignore
        except TypeError:
            return -1, -1, -1, -1

    def get_icon_coords_ru(self, button: ru) -> tuple[float, float]:
        dir: keys = "ru"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

    def get_icon_coords_mutl(self, button: mutl) -> tuple[float, float]:
        dir: keys = "mutl"
        path: str = self.image_repository[dir][button]
        try:
            x, y = locateCenterOnScreen(path)  # type: ignore
            return x, y  # type: ignore
        except TypeError:
            return -1, -1

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
