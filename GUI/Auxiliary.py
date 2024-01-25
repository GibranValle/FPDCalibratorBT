from customtkinter import CTk, CTkFrame, CTkButton, DISABLED  # type: ignore
from GUI.constants import *


class Auxiliary(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_auxiliary = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_auxiliary
        output = app.font_title
        self.app = app

        self.button_ment_mode = CTkButton(
            f,
            font=output,
            text="Enable m mode",
            command=lambda: self.action("enable"),
        )
        self.button_toggle_HVL = CTkButton(
            f,
            font=output,
            text="Toggle HVL",
            command=lambda: self.action("hlv"),
        )
        self.button_toggle_MAG = CTkButton(
            f,
            font=output,
            text="Toggle MAG",
            command=lambda: self.action("mag"),
        )
        self.select_calib = CTkButton(
            f,
            font=output,
            text="Select Calibrations",
            command=lambda: self.action("select"),
            state=DISABLED,
            text_color=DISABLED_COLOR,
        )
        self.calib_button = CTkButton(
            f,
            font=output,
            text="Push AWS Calib button",
            command=lambda: self.action("calib"),
        )
        self.FPD_calib = CTkButton(
            f,
            font=output,
            text="Push AWS Field calib",
            command=lambda: self.action("fpd"),
        )

        self.serial = app.com
        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=1)
        f.grid_columnconfigure(2, weight=1)
        f.rowconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)

        self.button_ment_mode.grid(row=0, column=0, pady=(10, 5), sticky="NSEW", padx=(10, 5))  # type: ignore
        self.button_toggle_HVL.grid(row=0, column=1, pady=(10, 5), sticky="NSEW", padx=5)  # type: ignore
        self.button_toggle_MAG.grid(row=0, column=2, pady=(10, 5), sticky="NSEW", padx=(5, 10))  # type: ignore
        self.select_calib.grid(row=1, column=0, pady=(5, 10), sticky="NSEW", padx=(10, 5))  # type: ignore
        self.calib_button.grid(row=1, column=1, pady=(5, 10), sticky="NSEW", padx=5)  # type: ignore
        self.FPD_calib.grid(row=1, column=2, pady=(5, 10), sticky="NSEW", padx=(5, 10))  # type: ignore
        self.show()

    def action(self, button: aux_option) -> None:
        if button == "enable":
            self.app.mu_interactor.enable_ment_mode()

        elif button == "hlv":
            self.app.mu_interactor.toggle_HVL()

        elif button == "mag":
            self.app.mu_interactor.toggle_MAG()

        elif button == "select":
            self.app.open_toplevel()

        elif button == "calib":
            self.app.aws_interactor.click_calib_button()

        elif button == "fpd":
            self.app.aws_interactor.click_field_button()

    def show(self):
        self.frame_auxiliary.grid(row=0, column=1, columnspan=3, sticky="NSEW", padx=(10, 20), pady=(20, 10))  # type: ignore

    def hide(self):
        self.frame_auxiliary.grid_forget()
