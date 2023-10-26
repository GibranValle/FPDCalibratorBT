from customtkinter import CTk, CTkFrame, CTkLabel, TOP, BOTH, BOTTOM, END, LEFT  # type: ignore
from GUI.constants import *


class Output(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_output = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_output
        text = app.font_output
        self.app = app
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

    def clear_all(self):
        self.output_a.configure(text=" ")  # type: ignore
        self.output_b.configure(text=" ")  # type: ignore

    def in_pause(self, secs: int):
        time = self.convert_seconds(secs)
        self.output_a.configure(text="Pause button pushed")  # type: ignore
        self.output_b.configure(text=f"time waited: {time}")  # type: ignore

    def waiting_ready(self, secs: int):
        time = self.convert_seconds(secs)
        self.output_a.configure(text="Waiting for ready signal")  # type: ignore
        self.output_b.configure(text=f"time waited: {time}")  # type: ignore

    def waiting_exposure_start(self, secs: int):
        time = self.convert_seconds(secs)
        self.output_a.configure(text="Waiting for exposure start")  # type: ignore
        self.output_b.configure(text=f"time waited: {time}")  # type: ignore

    def waiting_exposure_end(self, secs: int):
        time = self.convert_seconds(secs)
        self.output_a.configure(text="Waiting for exposure end")  # type: ignore
        self.output_b.configure(text=f"time waited: {time}")  # type: ignore

    def exposure_success(self, secs: int):
        time = self.convert_seconds(secs)
        self.output_a.configure(text="Exposure completed!")  # type: ignore
        self.output_b.configure(text=f"total time waited: {time}")  # type: ignore

    def exposure_aborted(self, secs: int):
        time = self.convert_seconds(secs)
        self.output_a.configure(text="Exposure aborted!")  # type: ignore
        self.output_b.configure(text=f"total time used: {time}")  # type: ignore

    @staticmethod
    def convert_seconds(secs: int) -> str:
        temp = secs
        if secs >= 3600:
            hours = int(secs / 3600)
            temp -= secs - 3600 * hours
            mins = int(temp / 60)
            sec = temp % 60
            return f"{hours}h {mins}m {sec}s"
        if secs >= 60:
            mins = int(secs / 60)
            sec = secs % 60
            return f"{mins}m {sec}s"
        return f"{secs}s"
