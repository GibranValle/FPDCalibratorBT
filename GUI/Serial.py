from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, LEFT, TOP, BOTH, DISABLED, NORMAL  # type: ignore
from GUI.constants import *
from threading import Thread
from time import sleep


class Serial(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_serial = CTkFrame(app, fg_color=BG_COLOR_1)
        self.label_serial = CTkLabel(
            self.frame_serial,
            text="Offline",
            font=app.font_text,
            fg_color=ERR_COLOR,
            width=125,
            corner_radius=5,
        )
        self.button_serial = CTkButton(
            self.frame_serial,
            command=lambda: self.toggle_serial(),
            font=app.font_text,
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            text="Connect",
            width=125,
        )
        self.serial = app.com
        self.frame_serial.columnconfigure(0, weight=1)
        self.frame_serial.columnconfigure(1, weight=1)
        self.label_serial.grid(row=0, column=0, padx=PADX_INSIDE_FRAME, pady=PADY_INSIDE_LAST)  # type: ignore
        self.button_serial.grid(row=0, column=1, padx=PADX_INSIDE_FRAME, pady=PADY_INSIDE_LAST)  # type: ignore
        self.show()

    def toggle_serial(self):
        if self.serial.is_offline() and not self.serial.is_listening():
            # stablish communication
            try:
                serialThread = Thread(target=self.serial.startListening)
                serialThread.start()
            except ConnectionError:
                return
            else:
                sleep(1.5)
                self.label_serial.configure(text="Online", fg_color=OK_COLOR)  # type: ignore
                self.button_serial.configure(text="Disconnect", fg_color=ERR_COLOR, hover_color=ERR_COLOR_HOVER)  # type: ignore
        elif not self.serial.is_offline() and self.serial.is_listening():
            # close comm
            try:
                self.serial.endListening()
            except ConnectionError:
                return
            else:
                self.label_serial.configure(text="Offline", fg_color=ERR_COLOR)  # type: ignore
                self.button_serial.configure(text="Connect", fg_color=OK_COLOR, hover_color=OK_COLOR_HOVER)  # type: ignore

    def show(self):
        self.frame_serial.pack(pady=PADY_FRAME, padx=10, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_serial.pack_forget()
