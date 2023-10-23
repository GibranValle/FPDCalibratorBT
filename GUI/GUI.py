from customtkinter import CTk, set_appearance_mode, set_default_color_theme  # type: ignore
from GUI.Serial import Serial
from SerialCom.SerialCom import SerialCom
from GUI.Tabs import Tabs
from GUI.constants import tabs_list, class_option, level_option
from GUI.Manual import Manual
from GUI.Output import Output
from Logger.Logger import Logger

# theme settings
set_appearance_mode("dark")
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(CTk):
    font_title: tuple[str, int, str] = ("Consolas", 18, "bold")
    font_text: tuple[str, int] = ("Consolas", 16)
    font_output: tuple[str, int] = ("Consolas", 13)

    def __init__(self) -> None:
        super().__init__()  # type: ignore
        self.logger = Logger()
        # Make the window jump above all
        self.attributes("-topmost", True)  # type: ignore
        self.geometry("300x350")  # type: ignore
        self.title("FPD Calibration bot")  # type: ignore
        self.resizable(False, False)  # type: ignore
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # type: ignore
        self.main = None
        self.com = SerialCom(self)
        # frames
        self.serial = Serial(self)
        self.tabs = Tabs(self)
        self.selected_tab = "manual"
        self.output = Output(self)
        self.manual = Manual(self)
        self.log("gui", "info", "Gui initialization completed")

    def change_tab(self, tab: tabs_list):
        self.selected_tab = tab

    def on_closing(self):
        try:
            self.com.endListening()
            self.destroy()
        except ConnectionError or ConnectionAbortedError:
            self.log("gui", "error", "error during closing port")

    def log(self, _class: class_option, level: level_option, note: str):
        self.logger.append(_class, level, note)
