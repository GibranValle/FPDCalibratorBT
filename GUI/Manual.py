from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, TOP, BOTH, END  # type: ignore
from GUI.constants import *
from threading import Thread


class Manual(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_manual = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_manual
        self.app = app
        text = app.font_text
        title = app.font_title
        self.com = app.com
        self.output = app.output

        self.label_manual = CTkLabel(f, font=title, text="Manual mode")

        self.button_release = CTkButton(
            f,
            font=text,
            text="Release",
            width=WIDTH_3,
            fg_color=ERR_COLOR,
            hover_color=ERR_COLOR_HOVER,
            command=lambda: self.action("release"),
        )
        self.button_short = CTkButton(
            f,
            font=text,
            text="1 Short",
            width=WIDTH_3,
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.action("short"),
        )

        self.button_long = CTkButton(
            f,
            font=text,
            text="1 Long",
            width=WIDTH_3,
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.action("long"),
        )

        self.serial = app.com
        self.frame_manual.grid_columnconfigure(0, weight=1)
        self.frame_manual.grid_columnconfigure(1, weight=1)
        self.label_manual.grid(row=0, column=0, columnspan=2, pady=PADY_INSIDE_FRAME, padx=PADX)  # type: ignore
        self.button_release.grid(row=1, column=0, columnspan=2, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_RIGHT)  # type: ignore
        self.button_short.grid(row=2, column=0, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_LEFT)  # type: ignore
        self.button_long.grid(row=2, column=1, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_RIGHT)  # type: ignore
        self.show()

    def action(self, button: push_option | exposure_option):
        try:
            if button == "release":
                self.app.change_app_state("stop")
                Thread(target=self.app.smart.end_exposure).start()
            elif button == "short":
                self.app.change_app_state("start")
                Thread(target=self.app.smart.start_short_exposure).start()
            elif button == "long":
                self.app.change_app_state("start")
                Thread(target=self.app.smart.start_long_exposure).start()

        except ConnectionError:
            self.app.log("manual", "error", "Connection error")
            self.output.change_a("Communication error")
            self.output.change_b("device not responding...")

    def show(self):
        self.frame_manual.pack(pady=PADY_FRAME, padx=PADX, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_manual.pack_forget()
