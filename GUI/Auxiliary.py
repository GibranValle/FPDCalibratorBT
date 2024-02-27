from customtkinter import CTk, CTkFrame, CTkButton, DISABLED  # type: ignore
from GUI.constants import *

TM = 10
BM = 10
INTER_Y_M = 5
LM = 10
RM = 10
INTER_X_M = 5


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

        self.FF_GEN = CTkButton(
            f,
            font=output,
            text="FF_Gen_Tools",
            command=lambda: self.action("ff"),
        )

        self.MCU0 = CTkButton(
            f,
            font=output,
            text="Open MCUO MUTL",
            command=lambda: self.action("mcu0"),
        )

        self.MU0 = CTkButton(
            f,
            font=output,
            text="Open MU0 MUTL",
            command=lambda: self.action("mu0"),
        )

        self.serial = app.com
        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=1)
        f.grid_columnconfigure(2, weight=1)
        f.rowconfigure(0, weight=1, minsize=20)
        f.rowconfigure(2, weight=1, minsize=20)
        f.rowconfigure(1, weight=1, minsize=20)

        self.button_ment_mode.grid(row=0, column=0, pady=(TM, INTER_Y_M), sticky="NSEW", padx=(LM, INTER_X_M))  # type: ignore
        self.button_toggle_HVL.grid(row=0, column=1, pady=(TM, INTER_Y_M), sticky="NSEW", padx=(INTER_X_M))  # type: ignore
        self.button_toggle_MAG.grid(row=0, column=2, pady=(TM, INTER_Y_M), sticky="NSEW", padx=(INTER_X_M, RM))  # type: ignore
        self.select_calib.grid(row=1, column=0, pady=(INTER_Y_M), sticky="NSEW", padx=(LM, INTER_X_M))  # type: ignore
        self.calib_button.grid(row=1, column=1, pady=(INTER_Y_M), sticky="NSEW", padx=(INTER_X_M))  # type: ignore
        self.FPD_calib.grid(row=1, column=2, pady=(INTER_Y_M), sticky="NSEW", padx=(INTER_X_M, RM))  # type: ignore
        self.FF_GEN.grid(row=2, column=0, pady=(INTER_Y_M, BM), sticky="NSEW", padx=(LM, INTER_X_M))  # type: ignore
        self.MCU0.grid(row=2, column=1, pady=(INTER_Y_M, BM), sticky="NSEW", padx=(INTER_X_M))  # type: ignore
        self.MU0.grid(row=2, column=2, pady=(INTER_Y_M, BM), sticky="NSEW", padx=(INTER_X_M, RM))  # type: ignore

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

        elif button == "ff":
            self.app.aws_interactor.openFF_Gen()

        elif button == "mcu0":
            self.app.mcu_interactor.open_MUTL_MCU()

        elif button == "mu0":
            self.app.mu_interactor.open_MUTL_MU()

    def show(self):
        self.frame_auxiliary.grid(row=0, column=1, rowspan=2, columnspan=3, sticky="NSEW", padx=(10, 20), pady=(20, 10))  # type: ignore

    def hide(self):
        self.frame_auxiliary.grid_forget()
