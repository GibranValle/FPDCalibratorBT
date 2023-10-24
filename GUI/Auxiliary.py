from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, TOP, BOTH, END, NORMAL, DISABLED  # type: ignore
from GUI.constants import *
from threading import Thread


class Auxiliary(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_auxiliary = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_auxiliary
        output = app.font_output
        text = app.font_text
        title = app.font_title
        self.com = app.com
        self.output = app.output
        self.logger = app.logger

        self.button_ment_mode = CTkButton(
            f,
            font=output,
            text="Enable m mode",
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.action("start"),
        )
        self.button_toggle_HVL = CTkButton(
            f,
            font=output,
            text="Toggle HVL",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.action("pause"),
        )
        self.button_toggle_MAG = CTkButton(
            f,
            font=output,
            text="Toggle MAG",
            fg_color=ERR_COLOR,
            hover_color=ERR_COLOR_HOVER,
            command=lambda: self.action("stop"),
        )

        self.serial = app.com
        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=1)
        f.grid_columnconfigure(2, weight=1)
        self.button_ment_mode.grid(row=0, column=0, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_toggle_HVL.grid(row=0, column=1, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_toggle_MAG.grid(row=0, column=2, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        # self.show()

    def action(self, button: auto_option) -> None:
        print(button)

    def show(self):
        self.frame_auxiliary.pack(pady=PADY_FRAME, padx=PADX, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_auxiliary.pack_forget()
