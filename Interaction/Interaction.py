from Interaction.types_interaction import fractions
from pyautogui import moveTo, click, position
from time import sleep
from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import mutl, ru
import subprocess
from time import sleep
import win32gui as w
import win32con as c
from typing import Literal


class Interaction:
    from GUI.GUI import GUI

    available_programs = Literal["RuPcTool.exe", "MU", "MCU", "MUTL.exe"]
    available_windows = Literal["RU PC-TOOL", "MU0", "MCU0"]

    def __init__(self, app: GUI) -> None:
        self.cv = ComputerVision()
        self.app = app

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

    def _click_icon_mutl(self, button: mutl):
        x, y = self.cv.get_icon_coords_mutl(button)
        if x > 0 and y > 0:
            self._click_center(x, y, True)
            return
        self.app.log("gui", "error", "MUTL ICON NOT FOUND")

    def _click_icon_ru(self, button: ru):
        x, y = self.cv.get_icon_coords_ru(button)
        if x > 0 and y > 0:
            self._click_center(x, y, True)
            return
        self.app.log("gui", "error", "RU ICON NOT FOUND")

    @staticmethod
    def _changeWindow(name: available_windows) -> None:
        def handler(hwnd: int, active: str) -> None:
            if w.IsWindowVisible(hwnd):
                wname = w.GetWindowText(hwnd)
                if active in wname:
                    w.SetForegroundWindow(hwnd)
                    w.ShowWindow(hwnd, c.SW_NORMAL)

        print(f"Window {name} opened...")
        w.EnumWindows(handler, name)  # type: ignore
        sleep(1)

    def _openApp(self, appName: available_programs) -> bool:
        try:
            if appName == "RuPcTool.exe":
                route = "C:\Program Files\Fujifilm\FCR\TOOL\RuPcTool\\"  # type: ignore
                exe = "RuPcTool"
                args = ""
                subprocess.Popen(route + exe + args)
                self.app.log("gui", "info", "RUPCTOOL opening...")

            elif appName == "MU":
                route = "C:\Program Files\FujiFilm\FCR\TOOL\MUTL\\"  # type: ignore
                exe = "MUTL"
                args = " /IP:192.168.0.100 /RUNAME:MU0 /TYPE:FDR-2500A"
                subprocess.Popen(route + exe + args)
                self.app.log("gui", "info", "MU opening...")

            elif appName == "MCU":
                route = "C:\Program Files\FujiFilm\FCR\TOOL\MUTL\\"  # type: ignore
                exe = "MUTL"
                args = " /IP:192.168.0.101 /RUNAME:MCU0 /TYPE:FDR-3000DRL /FCR:C:\Program Files\FujiFilm\FCR\\"  # type: ignore
                subprocess.Popen(route + exe + args)
                self.app.log("gui", "info", "MCU opening...")

        except FileNotFoundError:
            self.app.log("gui", "error", "File not found")
            return False
        except OSError:
            self.app.log("gui", "error", "program not installed found")
            return False
        else:
            sleep(1)
            return True

    def closeApp(self, appName: available_programs):
        if self._process_exists(appName):
            subprocess.call(
                ["taskkill", "/F", "/IM", appName],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            sleep(1)
            return
        self.app.log("gui", "error", "Nothing closed")

    def _scanWindows():  # type: ignore
        file = open("windowNames.txt", "w")

        def handler(hwnd: int, param: str):
            if w.IsWindowVisible(hwnd):
                wname = w.GetWindowText(hwnd)
                size = len(wname)
                if size > 0:
                    file.writelines(wname + "\n")

        w.EnumWindows(handler, None)  # type: ignore
        file.close()

    @staticmethod
    def _process_exists(process_name: available_programs):
        call = "TASKLIST", "/FI", "imagename eq %s" % process_name
        # use build-in check_output right away
        output = subprocess.check_output(call)
        # print(output)
        output = output.decode("latin-1")
        # check in last line for process name
        last_line = output.strip().split("\r\n")[-1]
        # print(last_line)
        # print(last_line)
        # because Fail message could be translated
        test = last_line.lower().startswith(process_name.lower())
        return test
