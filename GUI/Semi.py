from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, TOP, BOTH, END, NORMAL, DISABLED  # type: ignore
from GUI.constants import *
from threading import Thread


class Semi(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_semi = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_semi
        text = app.font_text
        title = app.font_title
        self.app = app
        self.label_semi = CTkLabel(f, font=title, text="Semiauto mode")

        self.button_semi_start = CTkButton(
            f,
            font=text,
            text="\u23F5",
            width=WIDTH_3,
            fg_color=OK_COLOR,
            hover_color=OK_COLOR_HOVER,
            command=lambda: self.action("start"),
        )
        self.button_semi_pause = CTkButton(
            f,
            font=text,
            text="\u23F8",
            width=WIDTH_3,
            fg_color=INFO_COLOR,
            hover_color=INFO_COLOR_HOVER,
            command=lambda: self.action("pause"),
        )
        self.button_semi_stop = CTkButton(
            f,
            font=text,
            text="\u23F9",
            width=WIDTH_3,
            fg_color=ERR_COLOR,
            hover_color=ERR_COLOR_HOVER,
            command=lambda: self.action("stop"),
        )
        self.button_semi_continuous = CTkButton(
            f,
            font=title,
            text="\u21AC",
            width=WIDTH_3,
            command=lambda: self.action("continuos"),
        )

        self.serial = app.com
        self.frame_semi.grid_columnconfigure(0, weight=1)
        self.frame_semi.grid_columnconfigure(1, weight=1)
        self.frame_semi.grid_columnconfigure(2, weight=1)
        self.frame_semi.grid_columnconfigure(3, weight=1)
        self.label_semi.grid(row=0, column=0, columnspan=4, pady=PADY_INSIDE_FRAME, padx=PADX)  # type: ignore
        self.button_semi_start.grid(row=1, column=0, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_semi_pause.grid(row=1, column=1, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_semi_stop.grid(row=1, column=2, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        self.button_semi_continuous.grid(row=1, column=3, pady=PADY_INSIDE_LAST, sticky="we", padx=2)  # type: ignore
        # self.show()

    def action(self, button: auto_option) -> None:
        self.app.change_app_state(button)
        if button == "start":
            self.app.log('semi', 'info', 'Request exposure start...')
            self.button_semi_start.configure(state=DISABLED)  # type: ignore
            self.button_semi_pause.configure(state=NORMAL)  # type: ignore
            self.button_semi_stop.configure(state=NORMAL)  # type: ignore
            self.button_semi_continuous.configure(state=DISABLED)  # type: ignore
            Thread(target=self.app.smart.start_smart_exposure).start()
        elif button == "pause":
            self.app.log('semi', 'info', 'Request exposure pause...')
            self.button_semi_start.configure(state=NORMAL)  # type: ignore
            self.button_semi_pause.configure(state=DISABLED)  # type: ignore
            self.button_semi_stop.configure(state=NORMAL)  # type: ignore
            self.button_semi_continuous.configure(state=DISABLED)  # type: ignore
        elif button == "stop":
            self.app.log('semi', 'info', 'Request exposure stop...')
            self.button_semi_start.configure(state=NORMAL)  # type: ignore
            self.button_semi_pause.configure(state=NORMAL)  # type: ignore
            self.button_semi_stop.configure(state=NORMAL)  # type: ignore
            self.button_semi_continuous.configure(state=NORMAL)  # type: ignore
        elif button == "continuos":
            self.app.log('semi', 'info', 'Request loop start...')
            self.button_semi_start.configure(state=DISABLED)  # type: ignore
            self.button_semi_pause.configure(state=NORMAL)  # type: ignore
            self.button_semi_stop.configure(state=NORMAL)  # type: ignore
            self.button_semi_continuous.configure(state=DISABLED)  # type: ignore
            Thread(target=self.app.smart.start_smart_loop).start()

    def show(self):
        self.frame_semi.pack(pady=PADY_FRAME, padx=PADX, side=TOP, fill=BOTH)  # type: ignore

    def hide(self):
        self.frame_semi.pack_forget()
