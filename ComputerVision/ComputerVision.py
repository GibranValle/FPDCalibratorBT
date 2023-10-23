from pyautogui import locateCenterOnScreen
import json
from typing import Literal
from ComputerVision.cv_types import (
    status_gen,
    status_mcu,
    status_mu,
    aws,
    gen,
    mcu,
    mcu_opt,
    mcu_tabs,
    mu,
    mutl,
    mu_tabs,
    ru,
    keys,
)

fraction = Literal["1/4", "1/2", "3/4"]


class ComputerVision:
    def __init__(self):
        self.status_mu: status_mu = "offline"
        self.status_mcu: status_mcu = "offline"
        self.status_gen: status_gen = "idle"
        with open("./ComputerVision/image_repository.json") as file:
            self.image_repository = json.load(file)

    def _get_status(self, name: str):
        for key, folder in self.image_repository.items():
            if name in key:
                for status, path in folder.items():
                    try:
                        x, y = locateCenterOnScreen(path, confidence=0.85)  # type: ignore
                        setattr(self, f"{name}", status)
                    except TypeError:
                        print(f"{path}{name} icon not found")
                        pass
        return getattr(self, f"{name}")

    def get_mu_status(self) -> status_mu:
        return self._get_status("status_mu")

    def get_mcu_status(self) -> status_mcu:
        return self._get_status("status_mcu")

    def get_gen_status(self) -> status_gen:
        return self._get_status("status_gen")

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

    def get_icon_coords_mu(self, button: mu) -> tuple[float, float]:
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
