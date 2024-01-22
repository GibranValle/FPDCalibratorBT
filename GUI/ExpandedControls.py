from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkToplevel, DISABLED, NORMAL  # type: ignore
from GUI.constants import *
from typing import Any


class ExpandedControls(CTkToplevel):
    def __init__(self, *args: Any):  # type: ignore
        from GUI.GUI import GUI

        super().__init__(*args)  # type: ignore
        self.app: GUI = args[0]
        self.all: list[all_calibrations] = ALL_CALIBRATIONS  # type: ignore
        self.attributes("-topmost", True)  # type: ignore
        self.geometry("360x105")
        self.resizable(False, False)  # type: ignore
        title = self.app.font_title  # type: ignore

        self.frame_control = CTkFrame(self, fg_color=BG_COLOR_1)
        f = self.frame_control

        self.button_start = CTkButton(
            f,
            font=title,
            text="\u23F5",
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.action("start"),
        )
        self.button_pause = CTkButton(
            f,
            text_color="black",
            font=title,
            text="\u23F8",
            fg_color=WARNING_COLOR,
            hover_color=WARNING_COLOR_HOVER,
            command=lambda: self.action("pause"),
        )
        self.button_stop = CTkButton(
            f,
            font=title,
            text="\u23F9",
            fg_color=ERR_COLOR,
            hover_color=ERR_COLOR_HOVER,
            command=lambda: self.action("stop"),
        )
        self.button_expand = CTkButton(
            f,
            font=title,
            text="Expand",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.action("expand"),
        )
        self.button_continuous = CTkButton(
            f,
            font=title,
            text="\u21AC",
            command=lambda: self.action("continuos"),
        )
        self.label_output = CTkLabel(f, text="", font=title, text_color=WARNING_COLOR)

        self.frame_control.grid_columnconfigure(0, weight=1)
        self.frame_control.grid_columnconfigure(1, weight=1)
        self.frame_control.grid_columnconfigure(2, weight=1)
        self.frame_control.grid_columnconfigure(3, weight=1)

        self.frame_control.rowconfigure(0, weight=1)
        self.frame_control.rowconfigure(1, weight=1)

        self.button_start.grid(row=0, column=0, pady=(10, 5), padx=(10, 5), sticky="NSEW")  # type: ignore
        self.button_pause.grid(row=0, column=1, pady=(10, 5), padx=5, sticky="NSEW")  # type: ignore
        self.button_stop.grid(row=0, column=2, pady=(10, 5), padx=(5), sticky="NSEW")  # type: ignore
        self.button_continuous.grid(row=0, column=3, pady=(10, 5), padx=(5, 10), sticky="NSEW")  # type: ignore
        self.button_stop.configure(state=DISABLED)  # type: ignore
        self.label_output.grid(row=1, column=0, columnspan=4, pady=(5, 10), padx=(10), sticky="NSEW")  # type: ignore
        self.show()
        self.update_buttons(self.app.app_state)

    def action(self, button: control_option) -> None:
        self.label_output.configure(text="")  # type: ignore           
        self.update_buttons(button)
        self.app.control.action(button)

    def update_buttons(self, button: control_option):
        if button == "start":
            self.button_start.configure(state=DISABLED)  # type: ignore
            self.button_pause.configure(state=NORMAL)  # type: ignore
            self.button_stop.configure(state=NORMAL)  # type: ignore
            self.button_continuous.configure(state=DISABLED)  # type: ignore
        elif button == "pause":
            self.button_start.configure(state=NORMAL)  # type: ignore
            self.button_pause.configure(state=DISABLED)  # type: ignore
            self.button_stop.configure(state=NORMAL)  # type: ignore
            self.button_continuous.configure(state=DISABLED)  # type: ignore
        elif button == "stop":
            self.button_start.configure(state=NORMAL)  # type: ignore
            self.button_pause.configure(state=NORMAL)  # type: ignore
            self.button_stop.configure(state=DISABLED)  # type: ignore
            self.button_continuous.configure(state=NORMAL)  # type: ignore
        elif button == "continuos":
            self.button_start.configure(state=DISABLED)  # type: ignore
            self.button_pause.configure(state=NORMAL)  # type: ignore
            self.button_stop.configure(state=NORMAL)  # type: ignore
            self.button_continuous.configure(state=DISABLED)  # type: ignore

    def update_message(self, text: str):
        if "error" in text.lower():
            self.label_output.configure(text_color=WARNING_COLOR)  # type: ignore            
        else:
            self.label_output.configure(text_color="white")  # type: ignore            
        self.label_output.configure(text=text)  # type: ignore

    def show(self):
        self.frame_control.pack(padx=10, pady=10)  # type: ignore

    def hide(self):
        self.frame_control.pack_forget()
