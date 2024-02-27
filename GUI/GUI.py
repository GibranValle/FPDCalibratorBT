from customtkinter import CTk, CTkToplevel, set_appearance_mode, set_default_color_theme, DISABLED, NORMAL  # type: ignore
import sys
from GUI.constants import *
from os import getcwd


class GUI(CTk):
    # theme settings
    path = str(getcwd())
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")

    font_title: tuple[str, int, str] = ("Consolas", 18, "bold")
    font_text: tuple[str, int] = ("Consolas", 16)
    font_output: tuple[str, int] = ("Consolas", 13)
    font_textbox: tuple[str, int] = ("Consolas", 11)
    from GUI.constants import tabs_list, class_option, level_option, control_option

    def __init__(self) -> None:
        # use import inside constructor to avoid circular import
        from GUI.Serial import Serial
        from SerialCom.SerialCom import SerialCom
        from GUI.constants import control_option
        from GUI.Auxiliary import Auxiliary
        from GUI.Vision import Vision
        from GUI.Control import Control
        from GUI.Log import Log
        from Logger.Logger import Logger
        from Exposure.SmartExposure import SmartExposure
        from Exposure.ManualExposure import ManualExposure
        from GUI.Mode import Mode
        from Interaction.AWSGen import AWSGen
        from Interaction.MCU0 import MCU0
        from Interaction.MU0 import MU0

        super().__init__()  # type: ignore
        self.attributes("-topmost", True)  # type: ignore
        self.geometry("960x440")  # type: ignore
        self.title("FPD Calibration bot")  # type: ignore
        self.resizable(False, False)  # type: ignore
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # type: ignore
        self.lower()
        self.logger = Logger()

        # states
        self.app_state: control_option = "stop"
        self.duration: dur_option = "short"
        self.mode: mode_option = "FPD"
        self.click_ok: ok_option = "on"
        self.autoselect: ok_option = "off"
        self.selected_cal: list[all_calibrations] = []
        self.current_calib = "None"

        # functions
        self.com = SerialCom(self)

        # GUI
        self.grid_columnconfigure(0, weight=1, minsize=250)
        self.grid_columnconfigure(1, weight=1, minsize=200)
        self.grid_columnconfigure(2, weight=1, minsize=100)
        self.grid_columnconfigure(3, weight=1, minsize=250)
        self.rowconfigure(0, weight=1, minsize=90)
        self.rowconfigure(1, weight=1, minsize=90)
        self.rowconfigure(2, weight=1, minsize=120)
        self.rowconfigure(3, weight=1, minsize=60)
        # GUI COMPONENTS
        self.toplevel_window: CTkToplevel
        self.expanded_window: CTkToplevel
        self.vision = Vision(self)
        self.serial = Serial(self)  # type: ignore
        self.auxiliary = Auxiliary(self)
        self.modes = Mode(self)
        self.control = Control(self)
        self.output_log = Log(self)  # type: ignore

        self.aws_interactor = AWSGen(self)
        self.mu_interactor = MU0(self)
        self.mcu_interactor = MCU0(self)
        self.smart = SmartExposure(self)
        self.manual = ManualExposure(self)
        self.log("gui", "info", "Gui initialization completed")

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

    def change_current_calib(self, calib: str):
        self.vision.current_calib.configure(text=calib)  # type: ignore

    def toggle_select_button(self):
        if self.mode != "auto":
            self.auxiliary.select_calib.configure(text_color=DISABLED_COLOR, state=DISABLED)  # type: ignore
        else:
            self.auxiliary.select_calib.configure(text_color="white", state=NORMAL)  # type: ignore

    def open_toplevel(self):
        from GUI.TopLevelWindow import ToplevelWindow

        try:
            if not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(self)
                self.toplevel_window.focus_force()
        except AttributeError:
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.focus_force()
            self.update()
        else:
            self.toplevel_window.focus()

    def open_expanded(self):
        from GUI.ExpandedControls import ExpandedControls

        try:
            if not self.expanded_window.winfo_exists():
                self.expanded_window = ExpandedControls(self)
                self.expanded_window.focus_force()
        except AttributeError:
            self.expanded_window = ExpandedControls(self)
            self.expanded_window.focus_force()
            self.update()
        else:
            self.expanded_window.focus()

    def change_app_state(self, state: control_option) -> None:
        self.app_state = state

    def log(self, _class: class_option, level: level_option, note: str) -> None:
        self.logger.append(_class, level, note)
