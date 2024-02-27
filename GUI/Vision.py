from customtkinter import CTk, CTkFrame, CTkLabel  # type: ignore
from GUI.constants import *


class Vision(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_vision = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_vision
        title = app.font_title
        self.app = app
        self.vision_label = CTkLabel(f, font=title, text="Vision Artificial: ON")
        self.ventana_label = CTkLabel(f, font=title, text="AWS")
        self.status_label = CTkLabel(f, font=title, text="Blocked")
        self.current_calib = CTkLabel(f, font=title, text="None")

        self.frame_vision.grid_columnconfigure(0, weight=1)
        self.frame_vision.rowconfigure(0, weight=1)
        self.frame_vision.rowconfigure(1, weight=1)
        self.frame_vision.rowconfigure(2, weight=1)
        self.frame_vision.rowconfigure(3, weight=1)

        self.vision_label.grid(row=0, column=0, pady=(10, 5), sticky="W", padx=10)  # type: ignore
        self.ventana_label.grid(row=1, column=0, pady=(5, 5), sticky="W", padx=10)  # type: ignore
        self.status_label.grid(row=2, column=0, pady=(5, 5), sticky="W", padx=10)  # type: ignore
        self.current_calib.grid(row=3, column=0, pady=(5, 10), sticky="W", padx=10)  # type: ignore

        self.update()
        self.show()

    def update(self):
        self.status_label.configure(text="Status: " + self.app.app_state)  # type: ignore
        self.current_calib.configure(text="")  # type: ignore

        if self.app.mode == "FPD":
            self.ventana_label.configure(text="Ventana: AWS")  # type: ignore
        elif self.app.mode == "mA":
            self.ventana_label.configure(text="Ventana: Generator")  # type: ignore

        if self.app.mode != "manual":
            self.vision_label.configure(text="Vision Artificial: ON")  # type: ignore
        else:
            self.vision_label.configure(text="Vision Artificial: OFF")  # type: ignore
            self.ventana_label.configure(text="N/A")  # type: ignore
            self.status_label.configure(text="N/A")  # type: ignore
        if self.app.mode == 'auto':
            self.current_calib.configure(text="Current calib: " + self.app.current_calib)  # type: ignore


    def show(self):
        self.frame_vision.grid(row=3, column=0, columnspan=2, sticky="NSEW", padx=(20, 10), pady=(10, 20))  # type: ignore

    def hide(self):
        self.frame_vision.grid_forget()
