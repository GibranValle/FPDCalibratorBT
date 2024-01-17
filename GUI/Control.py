from customtkinter import CTk, CTkFrame, CTkButton # type: ignore
from GUI.constants import *
from threading import Thread


class Control(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_control = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_control
        self.app = app
        text = app.font_text
        self.com = app.com

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
        self.button_expand = CTkButton(
            f,
            font=text,
            text="expand",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.action("expand"),
        )

        self.serial = app.com
        self.frame_control.grid_columnconfigure(0, weight=1)
        self.frame_control.rowconfigure(0, weight=1)
        self.frame_control.rowconfigure(1, weight=1)
        self.frame_control.rowconfigure(2, weight=1)
        self.frame_control.rowconfigure(3, weight=1)

        self.button_auto_start.grid(row=0, column=0, pady=(10, 5), sticky="NSEW", padx=10)  # type: ignore
        self.button_auto_pause.grid(row=1, column=0, pady=5, sticky="NSEW", padx=10)  # type: ignore
        self.button_auto_stop.grid(row=2, column=0, pady=5, sticky="NSEW", padx=10)  # type: ignore
        self.button_expand.grid(row=3, column=0, pady=(5, 10), sticky="NSEW", padx=10)  # type: ignore

        self.show()

    def action(self, button: auto_option | str) -> None:
        if button == "start":
            self.app.change_app_state(button)
            self.app.log("auto", "info", "Request auto start...")
            self.button_auto_start.configure(state=DISABLED)  # type: ignore
            self.button_auto_pause.configure(state=NORMAL)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=DISABLED)  # type: ignore
            Thread(target=self.app.smart.start_auto_loop).start()
        elif button == "pause":
            self.app.change_app_state(button)
            self.app.log("auto", "info", "Request pause...")
            self.button_auto_start.configure(state=NORMAL)  # type: ignore
            self.button_auto_pause.configure(state=DISABLED)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=DISABLED)  # type: ignore
        elif button == "stop":
            self.app.change_app_state(button)
            self.app.log("auto", "info", "Request stop...")
            self.button_auto_start.configure(state=NORMAL)  # type: ignore
            self.button_auto_pause.configure(state=NORMAL)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=NORMAL)  # type: ignore

    def show(self):
        self.frame_control.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="NSEW")  # type: ignore

    def hide(self):
        self.frame_control.grid_forget()
