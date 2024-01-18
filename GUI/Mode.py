from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton  # type: ignore
from GUI.constants import *


class Mode(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_mode = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_mode
        self.app = app
        text = app.font_title
        self.com = app.com

        self.button_short = CTkButton(
            f,
            font=text,
            text="Corto 15s",
            width=WIDTH_3,
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.mode("short"),
        )

        self.button_long = CTkButton(
            f,
            font=text,
            text="Largo 5m",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.mode("long"),
        )
        self.button_mA = CTkButton(
            f,
            font=text,
            text="mA",
            fg_color=INFO_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.mode("mA"),
        )
        self.button_FPD = CTkButton(
            f,
            font=text,
            text="FPD",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.mode("FPD"),
        )

        self.button_ok = CTkButton(
            f,
            font=text,
            text="Autoclick ok",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.mode("ok"),
        )
        self.button_auto_select = CTkButton(
            f,
            font=text,
            text="Autostart calib",
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.mode("autostart"),
        )

        self.serial = app.com
        self.frame_mode.grid_columnconfigure(0, weight=1)
        self.frame_mode.grid_columnconfigure(1, weight=1)
        self.frame_mode.grid_columnconfigure(2, weight=1)
        self.frame_mode.rowconfigure(0, weight=1)
        self.frame_mode.rowconfigure(1, weight=1)

        self.button_short.grid(row=0, column=0, pady=(10, 5), sticky="NSEW", padx=(10, 5))  # type: ignore
        self.button_long.grid(row=1, column=0, pady=(5, 10), sticky="NSEW", padx=(10, 5))  # type: ignore
        self.button_FPD.grid(row=0, column=1, pady=(10, 5), sticky="NSEW", padx=5)  # type: ignore
        self.button_mA.grid(row=1, column=1, pady=(5, 10), sticky="NSEW", padx=5)  # type: ignore
        self.button_ok.grid(row=0, column=2, pady=(10, 5), sticky="NSEW", padx=(5, 10))  # type: ignore
        self.button_auto_select.grid(row=1, column=2, pady=(5, 10), sticky="NSEW", padx=(5, 10))  # type: ignore
        self.update()
        self.show()

    def mode(self, option: str) -> None:
        if option == "short":
            self.app.duration = "short"
            self.app.mode = "manual"
            self.app.autoselect = "off"
        elif option == "long":
            self.app.duration = "long"
            self.app.mode = "manual"
            self.app.autoselect = "off" 
        elif option == "mA":
            self.app.duration = "long"
            self.app.mode = "mA"
            self.app.autoselect = "off" 
        elif option == "FPD":
            self.app.duration = "short"
            self.app.mode = "FPD"
            self.app.autoselect = "off" 
        elif option == "ok":
            if self.app.click_ok == "on":
                self.app.click_ok = "off"
                self.button_ok.configure(text_color=DISABLED_COLOR)  # type: ignore
            elif self.app.click_ok == "off":
                self.app.click_ok = "on"
                self.button_ok.configure(text_color='white')  # type: ignore
        elif option == "autostart":
            if self.app.autoselect == "on":
                self.app.mode = "FPD"
                self.app.autoselect = "off"
                self.button_auto_select.configure(text_color=DISABLED_COLOR)  # type: ignore
            elif self.app.autoselect == "off":
                self.app.mode = "auto"
                self.app.autoselect = "on"
                self.button_auto_select.configure(text_color='white')  # type: ignore
        self.update()
        self.app.vision.update()

    def update(self) -> None:
        if self.app.duration == "short":
            self.button_short.configure(text_color="white")  # type: ignore
            self.button_long.configure(text_color=DISABLED_COLOR)  # type: ignore
        elif self.app.duration == "long":
            self.button_long.configure(text_color="white")  # type: ignore
            self.button_short.configure(text_color=DISABLED_COLOR)  # type: ignore
        if self.app.mode == "FPD":
            self.button_auto_select.configure(text_color=DISABLED_COLOR)  # type: ignore
            self.button_FPD.configure(text_color="white")  # type: ignore
            self.button_mA.configure(text_color=DISABLED_COLOR)  # type: ignore
        elif self.app.mode == "mA":
            self.button_auto_select.configure(text_color=DISABLED_COLOR)  # type: ignore
            self.button_mA.configure(text_color="white")  # type: ignore
            self.button_FPD.configure(text_color=DISABLED_COLOR)  # type: ignore
        elif self.app.mode == "manual":
            self.button_auto_select.configure(text_color=DISABLED_COLOR)  # type: ignore
            self.button_mA.configure(text_color=DISABLED_COLOR)  # type: ignore
            self.button_FPD.configure(text_color=DISABLED_COLOR)  # type: ignore
        elif self.app.mode == "auto":
            self.button_short.configure(text_color=DISABLED_COLOR)  # type: ignore
            self.button_long.configure(text_color=DISABLED_COLOR)  # type: ignore
            self.button_mA.configure(text_color=DISABLED_COLOR)  # type: ignore
            self.button_FPD.configure(text_color=DISABLED_COLOR)  # type: ignore            

    def show(self):
        self.frame_mode.grid(row=1, column=0, columnspan=3, sticky="NSEW", padx=(20, 10), pady=10)  # type: ignore

    # def hide(self):
    #     self.frame_mode.grid_forget()
