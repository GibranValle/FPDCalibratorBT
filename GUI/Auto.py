from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, TOP, BOTH, END, NORMAL, DISABLED  # type: ignore
from GUI.constants import *
from threading import Thread


class Auto(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_auto = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_auto
        output = app.font_output
        text = app.font_text
        title = app.font_title
        self.app = app
        self.label_auto = CTkLabel(f, font=title, text="Auto mode")

        self.button_calib_selector = CTkButton(
            f, font=output, text="Select Calibrations", command=self.selector
        )

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
            font=text,
            text="\u23F8",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
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
        self.button_auto_continuous = CTkButton(
            f,
            font=title,
            text="\u21AC",
            command=lambda: self.action("continuos"),
        )

        f.grid_rowconfigure(0, weight=1)
        f.grid_rowconfigure(1, weight=1)
        f.grid_rowconfigure(2, weight=1)

        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=1)
        f.grid_columnconfigure(2, weight=1)

        self.label_auto.grid(row=0, column=0, columnspan=3, pady=PADY_INSIDE_FRAME, padx=PADX)  # type: ignore
        self.button_calib_selector.grid(row=1, column=0, columnspan=3, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_INSIDE_FRAME)  # type: ignore
        self.button_auto_start.grid(row=2, column=0, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_auto_pause.grid(row=2, column=1, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_auto_stop.grid(row=2, column=2, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        # self.show()

    def selector(self) -> None:
        self.app.open_toplevel()

    def action(self, button: auto_option) -> None:
        self.app.change_app_state(button)
        if button == "start":
            self.app.log("auto", "info", "Request auto start...")
            self.button_auto_start.configure(state=DISABLED)  # type: ignore
            self.button_auto_pause.configure(state=NORMAL)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=DISABLED)  # type: ignore
            Thread(target=self.app.smart.start_auto_loop).start()
        elif button == "pause":
            self.app.log("auto", "info", "Request pause...")
            self.button_auto_start.configure(state=NORMAL)  # type: ignore
            self.button_auto_pause.configure(state=DISABLED)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=DISABLED)  # type: ignore
        elif button == "stop":
            self.app.log("auto", "info", "Request stop...")
            self.button_auto_start.configure(state=NORMAL)  # type: ignore
            self.button_auto_pause.configure(state=NORMAL)  # type: ignore
            self.button_auto_stop.configure(state=NORMAL)  # type: ignore
            self.button_auto_continuous.configure(state=NORMAL)  # type: ignore

    def show(self):
        self.frame_auto.pack(pady=PADY_FRAME, padx=PADX, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_auto.pack_forget()
