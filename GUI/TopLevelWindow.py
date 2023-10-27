from customtkinter import CTk, CTkToplevel, CTkLabel, CTkFrame, CTkButton, StringVar, CTkCheckBox, LEFT, END, TOP, BOTH  # type: ignore
from GUI.constants import *


class ToplevelWindow(CTkToplevel):
    def __init__(self, *args):  # type: ignore
        from GUI.GUI import GUI

        super().__init__(*args)  # type: ignore
        self.gui: GUI = args[0]
        self.all: list[all_calibrations] = ALL_CALIBRATIONS  # type: ignore
        self.attributes("-topmost", True)  # type: ignore
        self.geometry("300x500")
        self.label = CTkLabel(
            self, text="Select Calibration to run \n Close to save", font=self.gui.font_title  # type: ignore
        )
        self.label.pack(pady=5)  # type: ignore

        self.frame_buttons = CTkFrame(self, fg_color=BG_COLOR_1)
        self.basic_button = CTkButton(
            self.frame_buttons, text="BASIC", width=75, command=self.basic
        )
        self.basic_button.pack(padx=10, pady=10, side=LEFT)  # type: ignore
        self.tomo_button = CTkButton(
            self.frame_buttons, text="TOMO", width=75, command=self.tomo
        )
        self.tomo_button.pack(padx=10, pady=10, side=LEFT)  # type: ignore
        self.full_button = CTkButton(
            self.frame_buttons, text="FULL", width=75, command=self.full
        )
        self.full_button.pack(padx=10, pady=10, side=LEFT)  # type: ignore

        self.frame_buttons.pack(padx=10, pady=(5, 10))  # type: ignore
        self.createCheckbox()

    def createCheckbox(self):
        for option in self.all:
            name = "var" + option.replace(" ", "_")
            if option in self.gui.selected_cal:
                globals()[name] = StringVar(value="on")
            else:
                globals()[name] = StringVar(value="off")
            self.checkbox = CTkCheckBox(
                self,
                text=option,
                variable=globals()[name],
                onvalue="on",
                offvalue="off",
                command=self.checkbox_event,
            )
            self.checkbox.pack(pady=3, padx=10, side=TOP, fill=BOTH)  # type: ignore

    def basic(self):
        self.gui.selected_cal = BASIC_CALIBRATIONS
        for option in self.all:
            name = "var" + option.replace(" ", "_")
            if option in self.gui.selected_cal:
                globals()[name].set("on")
            else:
                globals()[name].set("off")

    def tomo(self):
        self.gui.selected_cal = TOMO_CALIBRATIONS
        for option in self.all:
            name = "var" + option.replace(" ", "_")
            if option in self.gui.selected_cal:
                globals()[name].set("on")
            else:
                globals()[name].set("off")

    def full(self):
        self.gui.selected_cal = FULL_CALIBRATIONS
        for option in self.all:
            name = "var" + option.replace(" ", "_")
            if option in self.gui.selected_cal:
                globals()[name].set("on")
            else:
                globals()[name].set("off")

    def checkbox_event(self):
        for option in self.all:
            name = "var" + option.replace(" ", "_")
            if globals()[name].get() == "on":
                if not option in self.gui.selected_cal:
                    self.gui.selected_cal.append(option)
            elif globals()[name].get() == "off":
                if option in self.gui.selected_cal:
                    self.gui.selected_cal.remove(option)
