from customtkinter import CTk, set_appearance_mode, set_default_color_theme  # type: ignore
from GUI.Serial import Serial
from SerialCom.SerialCom import SerialCom
from GUI.Tabs import Tabs
from GUI.constants import tabs_list, class_option, level_option, auto_option
from GUI.Manual import Manual
from GUI.Semi import Semi
from GUI.Output import Output
from Logger.Logger import Logger
from Smart.SmartExposure import SmartExposure
import sys

# theme settings
set_appearance_mode("dark")
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(CTk):
    font_title: tuple[str, int, str] = ("Consolas", 18, "bold")
    font_text: tuple[str, int] = ("Consolas", 16)
    font_output: tuple[str, int] = ("Consolas", 13)

    def __init__(self) -> None:
        super().__init__()  # type: ignore
        self.app_state: auto_option = "stop"
        # Make the window jump above all
        self.attributes("-topmost", True)  # type: ignore
        self.geometry("300x350")  # type: ignore
        self.title("FPD Calibration bot")  # type: ignore
        self.resizable(False, False)  # type: ignore
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # type: ignore
        self.logger = Logger()
        self.com = SerialCom(self)
        self.serial = Serial(self)
        self.tabs = Tabs(self)
        self.selected_tab = "manual"
        self.output = Output(self)
        self.manual = Manual(self)
        self.semi = Semi(self)
        self.smart_exposure = SmartExposure(self)
        self.log("gui", "info", "Gui initialization completed")

    def change_tab(self, tab: tabs_list):
        if tab == "manual":
            self.manual.show()
            self.semi.hide()
        elif tab == "semi":
            self.manual.hide()
            self.semi.show()

    def on_closing(self, event: int = 0):
        print("closing")
        try:
            self.com.endListening()
        except ConnectionError or ConnectionAbortedError:
            self.log("gui", "error", "error during closing port")
        finally:
            print("destroying")
            self.destroy()
            sys.exit()

    def change_app_state(self, state: auto_option):
        self.app_state = state

    def start_smart_exposure(self):
        print("start smart exposure")
        self.smart_exposure.start_smart_exposure()

    def log(self, _class: class_option, level: level_option, note: str):
        self.logger.append(_class, level, note)
