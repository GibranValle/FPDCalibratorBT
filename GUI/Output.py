from customtkinter import CTk, CTkFrame, CTkLabel, TOP, BOTH, BOTTOM, END, LEFT  # type: ignore
from GUI.constants import *
from typing import Any


class Output(CTk):
    def __init__(self, app: Any):
        super().__init__()  # type: ignore
        self.frame_output = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_output
        text = app.font_output
        self.output_a = CTkLabel(f, font=text, text="text output a", height=HEIGHT_3)
        self.output_b = CTkLabel(f, font=text, text="text output b", height=HEIGHT_3)

        self.frame_output.grid_columnconfigure(0, weight=1)
        self.output_a.grid(row=0, column=0, pady=PADY_INSIDE_FRAME, padx=PADX_INSIDE_FRAME, sticky="w")  # type: ignore
        self.frame_output.grid_columnconfigure(0, weight=1)
        self.output_b.grid(row=1, column=0, pady=PADY_INSIDE_LAST, padx=PADX_INSIDE_FRAME, sticky="w")  # type: ignore

        self.serial = app.com
        self.show()

    def show(self):
        self.frame_output.pack(pady=PADY_FRAME, padx=10, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_output.pack_forget()

    def change_a(self, message: str):
        self.output_a.configure(text=message)  # type: ignore

    def change_b(self, message: str):
        self.output_b.configure(text=message)  # type: ignore
