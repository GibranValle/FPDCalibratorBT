from customtkinter import CTk, CTkFrame, CTkButton, TOP, BOTH, END, NORMAL, DISABLED  # type: ignore
from GUI.constants import *


class Auxiliary(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_auxiliary = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_auxiliary
        output = app.font_output
        self.output = app.output
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
        self.button_calib_selector = CTkButton(
            f, font=output, text="Select Calibrations", command=self.selector
        )

        self.serial = app.com
        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=1)
        f.grid_columnconfigure(2, weight=1)
        f.grid_rowconfigure(0, weight=1)
        f.grid_rowconfigure(1, weight=1)
        self.button_ment_mode.grid(row=0, column=0, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_toggle_HVL.grid(row=0, column=1, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_toggle_MAG.grid(row=0, column=2, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_calib_selector.grid(row=1, column=0, columnspan=2, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore

        # self.show()

    def action(self, button: aux_option) -> None:
        print(button)
        if button == "enable":
            self.app.mu_interactor.enable_ment()

        elif button == "hlv":
            self.app.mu_interactor.toggle_HVL()

        elif button == "mag":
            self.app.mu_interactor.toggle_MAG()

    def selector(self) -> None:
        self.app.open_toplevel()

    def show(self):
        self.frame_auxiliary.pack(pady=PADY_FRAME, padx=PADX, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_auxiliary.pack_forget()
