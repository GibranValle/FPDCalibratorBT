from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, TOP, BOTH, END  # type: ignore
from GUI.constants import *


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
        self.count = 0

        self.label_manual = CTkLabel(f, font=title, text="Manual mode")

        self.button_push = CTkButton(
            f,
            font=text,
            text="Push",
            width=WIDTH_3,
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.action("push"),
        )
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
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.action("short"),
        )

        self.button_long = CTkButton(
            f,
            font=text,
            text="1 Long",
            width=WIDTH_3,
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.action("long"),
        )

        self.serial = app.com
        self.frame_manual.grid_columnconfigure(0, weight=1)
        self.frame_manual.grid_columnconfigure(1, weight=1)

        self.label_manual.grid(row=0, column=0, columnspan=2, pady=PADY_INSIDE_FRAME, padx=PADX)  # type: ignore

        self.button_push.grid(row=1, column=0, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_LEFT)  # type: ignore
        self.button_release.grid(row=1, column=1, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_RIGHT)  # type: ignore

        self.button_short.grid(row=2, column=0, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_LEFT)  # type: ignore
        self.button_long.grid(row=2, column=1, pady=PADY_INSIDE_LAST, sticky="we", padx=PADX_RIGHT)  # type: ignore

        self.show()

    def action(self, button: push_option | exposure_option):
        try:
            if button == "push":
                self.app.log('manual', 'info', 'Request exposure start...')
                self.output.change_a("Request exposure start...")
                self.output.change_b(" ")
                self.com.communicate("L")
                self.output.change_b("UNDER EXPOSURE...")
            elif button == "release":
                self.app.log('manual', 'info', 'Request exposure end...')
                self.output.change_a("Request exposure end...")
                self.output.change_b(" ")
                self.com.communicate("X")
                self.output.change_b("NOT EXPOSING...")
        except ConnectionError:
            self.app.log('manual', 'error', 'Connection error')
            self.output.change_a("Communication error")
            self.output.change_b("device not responding...")

    def show(self):
        self.frame_manual.pack(pady=PADY_FRAME, padx=PADX, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_manual.pack_forget()
