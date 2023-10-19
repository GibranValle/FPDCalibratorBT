from pyautogui import locateCenterOnScreen, click, position, moveTo, locateOnScreen
import json
from time import sleep
from cv_types import (
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


class ComputerVision:
    def __init__(self):
        self.status_mu: status_mu = "offline"
        self.status_mcu: status_mcu = "offline"
        self.status_gen: status_gen = "idle"
        with open("./computer_vision/image_repository.json") as file:
            self.image_repository = json.load(file)

    def get_status(self, name: str):
        for key, folder in self.image_repository.items():
            if name in key:
                for status, path in folder.items():
                    try:
                        x, y = locateCenterOnScreen(path)  # type: ignore
                        setattr(self, f"{name}", status)
                    except TypeError:
                        pass
        return getattr(self, f"{name}")

    def get_mu_status(self):
        return self.get_status("status_mu")

    def get_mcu_status(self):
        return self.get_status("status_mcu")

    def get_gen_status(self):
        return self.get_status("status_gen")

    def click_fraction(self, path: str, fraction: str):
        try:
            a, b = position()
            sleep(0.5)
            x, y, w, h = locateOnScreen(path, confidence=0.9)  # type: ignore
            if fraction == "1/5":
                x = x + w / 5  # type: ignore
                y = y + h / 2  # type: ignore
            elif fraction == "1/3":
                x = x + w / 3  # type: ignore
                y = y + h / 2  # type: ignore
            elif fraction == "1/2":
                x = x + w / 2  # type: ignore
                y = y + h / 2  # type: ignore
            elif fraction == "3/5":
                x = x + 3 * w / 5  # type: ignore
                y = y + h / 2  # type: ignore
            elif fraction == "3/4":
                x = x + 3 * w / 4  # type: ignore
                y = y + h / 2  # type: ignore
            elif fraction == "4/5":
                x = x + 4 * w / 5  # type: ignore
                y = y + h / 2  # type: ignore
            elif fraction == "2/3":
                x = x + 2 * w / 3  # type: ignore
                y = y + h / 2  # type: ignore
            click(x, y)  # type: ignore
            moveTo(a, b, 0.1)
            sleep(0.4)
        except TypeError:
            print("icon not found")

    def click_center(self, window: keys, button: str):
        path: str = self.image_repository[f"{window}"][f"{button}"]
        try:
            a, b = position()
            sleep(0.5)
            x, y = locateCenterOnScreen(path)  # type: ignore
            click(x, y)  # type: ignore
            moveTo(a, b, 0.1)
            sleep(0.4)
        except TypeError:
            print(f"{button} icon not found")

    def click_aws(self, button: aws):
        self.click_center("aws", button)

    def click_gen(self, button: gen):
        self.click_center("gen", button)

    def click_mu(self, button: mu):
        self.click_center("mu", button)

    def click_mcu(self, button: mcu):
        self.click_center("mcu", button)

    def click_mcu_opt(self, button: mcu_opt):
        self.click_center("mcu_opt", button)

    def click_ru(self, button: ru):
        self.click_center("ru", button)

    def click_mcu_calibration_tab(self):
        dir: keys = "mcu_tabs"
        button_a: mcu_tabs = "mcua"
        page_0: str = self.image_repository[dir][button_a]

        button_b: mcu_tabs = "mcub"
        page_1: str = self.image_repository[dir][button_b]

        button_c: mcu_tabs = "cal_selected"
        cal_selected: str = self.image_repository[dir][button_c]

        button_d: mcu_tabs = "cal_opt_selected"
        cal_opt_selected: str = self.image_repository[dir][button_d]

        # check if tab is already selected
        try:
            x, y = locateCenterOnScreen(cal_selected)  # type: ignore
            print("Calibration tab is already selected")
            return
        except TypeError:
            print("Calibration tab is not selected yet")

        # check if opt tab is already selected
        try:
            x, y = locateCenterOnScreen(cal_opt_selected)  # type: ignore
            print("Calibration tab opt is selected and cal visible")
            self.click_fraction(cal_opt_selected, "1/2")
            print("Calibration tab should be selected now")
            return
        except TypeError:
            print("Calibration tab is not selected yet")

        # check if already in page 1
        try:
            x, y = locateCenterOnScreen(page_1)  # type: ignore
            print("Calibration tab is visible")
            self.click_fraction(page_1, "1/2")
            print("Calibration tab should be selected now")
            return
        except TypeError:
            print("not in page 1")

        try:
            x, y = locateCenterOnScreen(page_0)  # type: ignore
            print("is page 0, clicking next...")
            a: keys = "mutl"
            b: mutl = "only_right"
            right: str = self.image_repository[a][b]
            x, y = locateCenterOnScreen(right)  # type: ignore
            click(x, y)  # type: ignore
        except TypeError:
            print("Calibration MCU Tab may be selected")
            try:
                x, y = locateCenterOnScreen(cal_selected)  # type: ignore
            except TypeError:
                print("MUTL MCU not visible")
                raise TypeError

        try:
            print("Should be now in page 1")
            x, y = locateCenterOnScreen(page_1)  # type: ignore
            self.click_fraction(page_1, "1/2")
            print("Calibration tab is selected")
        except TypeError:
            print("MUTL MCU not visible")
            raise TypeError

    def click_mcu_calibration_opt_tab(self):
        dir: keys = "mcu_tabs"
        button_a: mcu_tabs = "mcua"
        page_0: str = self.image_repository[dir][button_a]

        button_b: mcu_tabs = "mcub"
        page_1: str = self.image_repository[dir][button_b]

        button_c: mcu_tabs = "cal_selected"
        cal_selected: str = self.image_repository[dir][button_c]

        button_d: mcu_tabs = "cal_opt_selected"
        cal_opt_selected: str = self.image_repository[dir][button_d]

        # check if opt tab is already selected
        try:
            x, y = locateCenterOnScreen(cal_opt_selected)  # type: ignore
            print("Calibration tab opt is already selected")
            return
        except TypeError:
            print("Calibration tab opt is not selected yet")

        # check if tab is already selected
        try:
            x, y = locateCenterOnScreen(cal_selected)  # type: ignore
            print("Calibration tab is selected and cal opt visible")
            self.click_fraction(cal_selected, "3/4")
            print("Calibration tab should be selected now")
            return
        except TypeError:
            print("Calibration tab is not selected yet")

        # check if already in page 1
        try:
            x, y = locateCenterOnScreen(page_1)  # type: ignore
            print("Calibration tab is visible")
            self.click_fraction(page_1, "1/2")
            print("Calibration tab should be selected now")
            return
        except TypeError:
            print("not in page 1")

        try:
            x, y = locateCenterOnScreen(page_0)  # type: ignore
            print("is page 0, clicking next...")
            a: keys = "mutl"
            b: mutl = "only_right"
            right: str = self.image_repository[a][b]
            x, y = locateCenterOnScreen(right)  # type: ignore
            click(x, y)  # type: ignore
        except TypeError:
            print("Calibration MCU Tab may be selected")
            try:
                x, y = locateCenterOnScreen(cal_selected)  # type: ignore
            except TypeError:
                print("MUTL MCU not visible")
                raise TypeError

        try:
            print("Should be now in page 1")
            x, y = locateCenterOnScreen(page_1)  # type: ignore
            self.click_fraction(page_1, "1/2")
            print("Calibration tab is selected")
        except TypeError:
            print("MUTL MCU not visible")
            raise TypeError

    def click_mutl_mu_calibration(self):
        pass

    def click_mutl_mu_generator(self):
        pass


if __name__ == "__main__":
    cv = ComputerVision()
    s = cv.get_mu_status()
    try:
        cv.click_mcu_calibration_tab()
    except TypeError:
        print("general bug")

    try:
        cv.click_mcu_calibration_opt_tab()
    except TypeError:
        print("general bug")
