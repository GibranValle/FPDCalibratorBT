from customtkinter import CTk, CTkToplevel, CTkLabel, CTkFrame, CTkButton, StringVar, CTkCheckBox, LEFT, END, TOP, BOTH  # type: ignore
from GUI.constants import *
from threading import Thread


class ExpandedControls(CTkToplevel):
    def __init__(self, *args):  # type: ignore
        from GUI.GUI import GUI

        super().__init__(*args)  # type: ignore
        self.gui: GUI = args[0]
        self.all: list[all_calibrations] = ALL_CALIBRATIONS  # type: ignore
        self.attributes("-topmost", True)  # type: ignore
        self.geometry("300x200")
        text = self.gui.font_text  # type: ignore
        title = self.gui.font_title  # type: ignore
        self.label = CTkLabel(self, text="Control panel", font=title)
        self.label.pack(pady=5)  # type: ignore

        self.frame_buttons = CTkFrame(self, fg_color=BG_COLOR_1)
        f = self.frame_buttons
        self.button_auto_start = CTkButton(
            f,
            font=text,
            text="\u23F5",
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.action("start"),
        )
        self.button_auto_pause = CTkButton(
            f,
            text_color="black",
            font=text,
            text="\u23F8",
            fg_color=WARNING_COLOR,
            hover_color=WARNING_COLOR_HOVER,
            command=lambda: self.action("pause"),
        )
        self.button_auto_stop = CTkButton(
            f,
            font=text,
            text="\u23F9",
            fg_color=ERR_COLOR,
            hover_color=ERR_COLOR_HOVER,
            command=lambda: self.action("stop"),
        )
        self.button_loop = CTkButton(
            f,
            font=text,
            text="expand",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.action("expand"),
        )

    def action(self, button: auto_option | str) -> None:
        if button == "start":
            self.gui.change_app_state(button)
            self.gui.log("auto", "info", "Request auto start...")
            self.button_auto_start.configure(state=DISABLED)  # type: ignore
            self.button_auto_pause.configure(state=NORMAL)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=DISABLED)  # type: ignore
            Thread(target=self.gui.smart.start_auto_loop).start()
        elif button == "pause":
            self.gui.change_app_state(button)
            self.gui.log("auto", "info", "Request pause...")
            self.button_auto_start.configure(state=NORMAL)  # type: ignore
            self.button_auto_pause.configure(state=DISABLED)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=DISABLED)  # type: ignore
        elif button == "stop":
            self.gui.change_app_state(button)
            self.gui.log("auto", "info", "Request stop...")
            self.button_auto_start.configure(state=NORMAL)  # type: ignore
            self.button_auto_pause.configure(state=NORMAL)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=NORMAL)  # type: ignore
