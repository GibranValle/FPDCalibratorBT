from customtkinter import CTk, CTkFrame, CTkButton, LEFT, TOP, BOTH, DISABLED, NORMAL  # type: ignore
from GUI.constants import *


class Tabs(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_tabs = CTkFrame(app, fg_color=BG_COLOR_1)
        self.frame_tabs.grid_columnconfigure(0, weight=1)
        self.frame_tabs.grid_columnconfigure(1, weight=1)
        self.frame_tabs.grid_columnconfigure(2, weight=1)
        self.app = app

        self.tab_manual = CTkButton(
            self.frame_tabs,
            font=app.font_text,
            text="Manual",
            command=lambda: self.click_tab("manual"),
        )
        self.tab_semi = CTkButton(
            self.frame_tabs,
            font=app.font_text,
            text="Semi",
            command=lambda: self.click_tab("semi"),
        )
        self.tab_auto = CTkButton(
            self.frame_tabs,
            font=app.font_text,
            text="Auto",
            command=lambda: self.click_tab("auto"),
        )

        self.tab_manual.grid(row=0, column=0, padx=PADX_LEFT, sticky="ew", pady=5)  # type: ignore
        self.tab_semi.grid(row=0, column=1, padx=PADX_MIDDLE, pady=PADY_INSIDE_LAST, sticky="ew")  # type: ignore
        self.tab_auto.grid(row=0, column=2, padx=PADX_RIGHT, sticky="we", pady=PADY_INSIDE_LAST)  # type: ignore
        self.frame_tabs.pack(pady=PADY_FRAME, padx=PADX, side=TOP, fill=BOTH)  # type: ignore

    def click_tab(self, tab: tabs_list):
        self.app.change_tab(tab)
