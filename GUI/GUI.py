from customtkinter import CTk, set_appearance_mode, set_default_color_theme  # type: ignore
import sys

# theme settings
set_appearance_mode("dark")
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(CTk):
    font_title: tuple[str, int, str] = ("Consolas", 18, "bold")
    font_text: tuple[str, int] = ("Consolas", 16)
    font_output: tuple[str, int] = ("Consolas", 13)
    from GUI.constants import tabs_list, class_option, level_option, auto_option

    def __init__(self) -> None:
        # use import inside constructor to avoid circular import
        from GUI.Serial import Serial
        from SerialCom.SerialCom import SerialCom
        from GUI.Tabs import Tabs
        from GUI.constants import auto_option
        from GUI.Manual import Manual
        from GUI.Semi import Semi
        from GUI.Output import Output
        from Logger.Logger import Logger
        from Smart.SmartExposure import SmartExposure
        from GUI.Auto import Auto
        from GUI.Auxiliary import Auxiliary

        super().__init__()  # type: ignore
        self.app_state: auto_option = "stop"
        # Make the window jump above all
        self.attributes("-topmost", True)  # type: ignore
        self.geometry("350x350")  # type: ignore
        self.title("FPD Calibration bot")  # type: ignore
        self.resizable(False, False)  # type: ignore
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # type: ignore
        self.logger = Logger()
        self.com = SerialCom(self)
        self.serial = Serial(self)  # type: ignore
        self.tabs = Tabs(self)
        self.selected_tab = "manual"
        self.output = Output(self)
        self.manual = Manual(self)
        self.semi = Semi(self)
        self.auto = Auto(self)
        self.aux = Auxiliary(self)
        self.smart = SmartExposure(self)
        self.log("gui", "info", "Gui initialization completed")

    def change_tab(self, tab: tabs_list):
        if tab == "manual":
            self.manual.show()
            self.semi.hide()
            self.auto.hide()
            self.aux.hide()
        elif tab == "semi":
            self.manual.hide()
            self.semi.show()
            self.auto.hide()
            self.aux.hide()
        elif tab == "auto":
            self.manual.hide()
            self.semi.hide()
            self.auto.show()
            self.aux.show()

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

    def change_app_state(self, state: auto_option) -> None:
        self.app_state = state

    def log(self, _class: class_option, level: level_option, note: str) -> None:
        self.logger.append(_class, level, note)
