from customtkinter import CTk, CTkFrame, CTkLabel, CTkTextbox, END, CURRENT  # type: ignore
from GUI.constants import *


class Log(CTk):
    from GUI.GUI import GUI

    def __init__(self, app: GUI):
        super().__init__()  # type: ignore
        self.frame_log = CTkFrame(app, fg_color=BG_COLOR_1)
        f = self.frame_log
        title = app.font_title
        textbox = app.font_textbox
        self.app = app
        self.log_label = CTkLabel(f, font=title, text="LOG")
        self.textbox = CTkTextbox(
            master=f, corner_radius=0, text_color="white", font=textbox
        )
        self.frame_log.grid_columnconfigure(0, weight=1)
        self.frame_log.rowconfigure(0, weight=1)
        self.frame_log.rowconfigure(1, weight=1)
        self.log_label.grid(row=0, column=0, pady=(5, 0), sticky="NW", padx=10)  # type: ignore
        self.textbox.grid(row=1, column=0, pady=(0, 5), sticky="NSEW", padx=10)  # type: ignore
        self.show()

    def append(self, text: str) -> None:
        import re

        try:
            if self.app.expanded_window.winfo_exists():
                self.app.expanded_window.update_message(text)  # type: ignore
        except:
            pass
        if "error" in text.lower():
            self.log_label.configure(text_color=WARNING_COLOR, text="LOG ERROR!")  # type: ignore
        else:
            self.log_label.configure(text_color="white", text="LOG")  # type: ignore

        previousText = ""
        previousRaw = self.textbox.get("end-2l", "end")  # type: ignore
        previousMatch = re.search(r"(^\w.*):", previousRaw)
        if previousMatch != None:
            previousText = previousMatch.group(0)

        newText = "."
        match = re.search(r"(^\w.*):", text)
        if match != None:
            newText = match.group(0)

        if previousText == newText:
            self.textbox.delete("end-2l", "end-1l")  # type: ignore

        self.textbox.insert("end", f"{text}\n")  # type: ignore
        self.textbox.see("end")  # type: ignore

    def show(self):
        self.frame_log.grid(row=2, column=3, rowspan=2, sticky="NSEW", padx=(10, 20), pady=(10, 20))  # type: ignore

    def hide(self):
        self.frame_log.grid_forget()
