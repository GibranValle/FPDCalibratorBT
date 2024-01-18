from customtkinter import CTk, CTkFrame, CTkButton, DISABLED, NORMAL  # type: ignore
from GUI.constants import *
from threading import Thread


class Control(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_control = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_control
        self.app = app
        title = app.font_title
        self.com = app.com

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

        self.serial = app.com
        self.frame_control.grid_columnconfigure(0, weight=1)
        self.frame_control.grid_columnconfigure(1, weight=1)
        self.frame_control.grid_columnconfigure(2, weight=1)

        self.frame_control.rowconfigure(0, weight=1)
        self.frame_control.rowconfigure(1, weight=1)

        self.button_start.grid(row=0, column=0, pady=(10, 5), padx=(10, 5), sticky="NSEW")  # type: ignore
        self.button_pause.grid(row=0, column=1, pady=(10, 5), padx=5, sticky="NSEW")  # type: ignore
        self.button_stop.grid(row=0, column=2, pady=(10, 5), padx=(5, 10), sticky="NSEW")  # type: ignore
        self.button_expand.grid(row=1, column=0, columnspan=2, pady=(5, 10), padx=(10, 5), sticky="NSEW")  # type: ignore
        self.button_continuous.grid(row=1, column=2, pady=(5, 10), padx=(5, 10), sticky="NSEW")  # type: ignore
        self.button_stop.configure(state=DISABLED)  # type: ignore
        self.show()

    def action(self, button: auto_option | str) -> None:
        if button == "start":
            self.app.change_app_state(button)
            self.app.output_log.append("Request start...")
            self.app.log("auto", "info", "Request start...")
            self.button_start.configure(state=DISABLED)  # type: ignore
            self.button_pause.configure(state=NORMAL)  # type: ignore
            self.button_stop.configure(state=NORMAL)  # type: ignore
            self.button_continuous.configure(state=DISABLED)  # type: ignore
            Thread(target=self.app.smart.start_auto_loop).start()
        elif button == "pause":
            self.app.change_app_state(button)
            self.app.output_log.append("Request pause...")
            self.app.log("auto", "info", "Request pause...")
            self.button_start.configure(state=NORMAL)  # type: ignore
            self.button_pause.configure(state=DISABLED)  # type: ignore
            self.button_stop.configure(state=NORMAL)  # type: ignore
            self.button_continuous.configure(state=DISABLED)  # type: ignore
        elif button == "stop":
            self.app.change_app_state(button)
            self.app.output_log.append("Request stop...")
            self.app.log("auto", "info", "Request stop...")
            self.button_start.configure(state=NORMAL)  # type: ignore
            self.button_pause.configure(state=NORMAL)  # type: ignore
            self.button_stop.configure(state=DISABLED)  # type: ignore
            self.button_continuous.configure(state=NORMAL)  # type: ignore
        if button == "continuos":
            self.app.change_app_state(button)
            self.app.output_log.append("Request loop start...")
            self.app.log("auto", "info", "Request loop start...")
            self.button_start.configure(state=DISABLED)  # type: ignore
            self.button_pause.configure(state=NORMAL)  # type: ignore
            self.button_stop.configure(state=NORMAL)  # type: ignore
            self.button_continuous.configure(state=DISABLED)  # type: ignore
            Thread(target=self.app.smart.start_auto_loop).start()            

    def show(self):
        self.frame_control.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="NSEW")  # type: ignore

    def hide(self):
        self.frame_control.grid_forget()