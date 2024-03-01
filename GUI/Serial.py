from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton  # type: ignore
from GUI.constants import *
from threading import Thread
from time import sleep


class Serial(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_serial = CTkFrame(app, fg_color=BG_COLOR_1)
        self.app = app

        self.label_serial = CTkLabel(
            self.frame_serial,
            text="Conexión Serial",
            font=app.font_title,
        )

        self.fixed_label = CTkLabel(
            self.frame_serial,
            text="Status: ",
            font=app.font_title,
        )

        self.status_serial = CTkLabel(
            self.frame_serial,
            text="Offline",
            font=app.font_title,
            text_color=ERR_COLOR_LIGHT,
        )

        self.button_serial = CTkButton(
            self.frame_serial,
            command=lambda: self.toggle_serial(),
            font=app.font_title,
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            text="Connect",
            width=125,
        )
        self.serial = app.com
        self.frame_serial.columnconfigure(0, weight=1)
        self.frame_serial.columnconfigure(1, weight=1)
        self.frame_serial.rowconfigure(0, weight=1)
        self.frame_serial.rowconfigure(1, weight=1)
        self.frame_serial.rowconfigure(2, weight=1)
        self.label_serial.grid(row=0, column=0, padx=10, sticky="NSEW", pady=(5, 0), columnspan=2)  # type: ignore
        self.fixed_label.grid(row=1, column=0, padx=(10, 5), sticky="W", pady=5)  # type: ignore
        self.status_serial.grid(row=1, column=1, padx=(5, 10), sticky="E", pady=5)  # type: ignore
        self.button_serial.grid(row=2, column=0, padx=10, sticky="NSEW", pady=(0, 5), columnspan=2)  # type: ignore
        self.show()

    def toggle_serial(self) -> None:
        if self.serial.is_offline() and not self.serial.is_listening():
            # stablish communication
            try:
                serialThread = Thread(target=self.serial.startListening)
                serialThread.start()
            except ConnectionError:
                return
            else:
                sleep(1.5)
                if self.serial.is_offline():
                    self.app.window_log("Error: USB no conectado")
                    print("arduino not found!")
                    return
                
                if not self.serial.communicate('T'):
                    self.app.window_log("Error: Disparador no responde")
                    print("arduino not responding!")
                    return
                
                self.status_serial.configure(text="Online", text_color=OK_COLOR)  # type: ignore
                self.button_serial.configure(text="Disconnect", fg_color=ERR_COLOR, hover_color=ERR_COLOR_HOVER)  # type: ignore
                self.app.window_log("Disparador Online!")

        elif not self.serial.is_offline() and self.serial.is_listening():
            # close comm
            if not self.serial.endListening():
                return

            self.status_serial.configure(text="Offline", text_color=ERR_COLOR_LIGHT)  # type: ignore
            self.button_serial.configure(text="Connect", fg_color=OK_COLOR, hover_color=OK_COLOR_HOVER)  # type: ignore

    def show(self):
        self.frame_serial.grid(row=0, column=0, rowspan=2, sticky="NSEW", padx=(20, 10), pady=(20, 10))  # type: ignore

    def hide(self):
        self.frame_serial.grid_forget()
