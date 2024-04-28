from customtkinter import CTk, CTkFrame, CTkLabel  # type: ignore
from GUI.constants import *


class StatusBox(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_vision = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_vision
        title = app.font_title
        self.app = app

        self.status_mu_label = CTkLabel(
            f, font=title, text="MU: Blocked", text_color="red"
        )
        self.status_gen_label = CTkLabel(
            f, font=title, text="Gen: Blocked", text_color="red"
        )
        self.current_calib = CTkLabel(f, font=title, text="None")
        self.status_mcu_label = CTkLabel(f, font=title, text="MCU: Offline")

        self.frame_vision.grid_columnconfigure(0, weight=1)
        self.frame_vision.rowconfigure(0, weight=1)
        self.frame_vision.rowconfigure(1, weight=1)
        self.frame_vision.rowconfigure(2, weight=1)
        self.frame_vision.rowconfigure(3, weight=1)

        self.status_gen_label.grid(row=0, column=0, pady=(10, 5), sticky="W", padx=10)  # type: ignore
        self.status_mu_label.grid(row=1, column=0, pady=(5, 5), sticky="W", padx=10)  # type: ignore
        self.status_mcu_label.grid(row=2, column=0, pady=(5, 5), sticky="W", padx=10)  # type: ignore
        self.current_calib.grid(row=3, column=0, pady=(5, 10), sticky="W", padx=10)  # type: ignore

        self.update()
        self.show()

    def update(self):
        self.status_gen_label.configure(text="")  # type: ignore
        self.status_mu_label.configure(text="MU: " + self.app.get_state_mu())  # type: ignore
        self.current_calib.configure(text="")  # type: ignore
        self.status_mcu_label.configure(text="MCU: " + self.app.get_state_mcu())  # type: ignore

        if self.app.mode == "mA":
            self.status_gen_label.configure(text="Gen: " + self.app.get_state_gen(), text_color="white")  # type: ignore

        if self.app.mode == "manual":
            self.status_mcu_label.configure(text="")  # type: ignore
            self.status_mu_label.configure(text="")  # type: ignore
        if self.app.mode == "auto":
            self.current_calib.configure(text="Current calib: " + self.app.current_calib)  # type: ignore

    def show(self):
        self.frame_vision.grid(row=3, column=0, columnspan=2, sticky="NSEW", padx=(20, 10), pady=(10, 20))  # type: ignore

    def hide(self):
        self.frame_vision.grid_forget()
