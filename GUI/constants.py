from typing import Literal, get_args
import customtkinter as ck  # type: ignore

HEIGHT_1 = 50
HEIGHT_2 = 40
HEIGHT_3 = 15
WIDTH_1 = 240
WIDTH_2 = 180
WIDTH_3 = 60
WIDTH_4 = 70

BG_COLOR_0 = "#242424"
BG_COLOR_1 = "#353535"
OK_COLOR = "#388731"
OK_COLOR_HOVER = "#286123"
INFO_COLOR = "#003366"
INFO_COLOR_HOVER = "#002255"
ERR_COLOR = "#880015"
ERR_COLOR_HOVER = "#6E0011"
DISABLED_COLOR = "#555555"

PLAY = "\u23F5"
PAUSE = "\u23F8"
STOP = "\u23F9"

MAX_EXP_DURATION = 15
MAX_MA_EXP_DURATION = 360
PREP_EXP_TIME = 1200
TIME_BTW_EXP = 30

CALIB_TYPE = Literal["ma_calib", "manual", "auto"]
KIND = Literal["Short", "Long", "Exposure", "Set"]
BUTTONS = Literal["start", "stop", "pause"]

aws_status = Literal[
    "isCalibratingFPD",
    "isWaitingOk",
    "isStdBy",
    "isBlocked",
    "isExposing",
    "isCalibPass",
    "isExposureDone",
]
AWS_STATUS = get_args(aws_status)

tabs_list = Literal["manual", "semi", "auto"]
push_option = Literal["push", "release"]
class_option = Literal["manual", "semi", "auto", "serial", "gui"]
level_option = Literal["info", "error", "warning"]


PADY_FRAME = 10, 0
PADY_END = 10
PADX_INSIDE_FRAME = 10
PADY_INSIDE_FRAME = (5, 0)
PADY_INSIDE_LAST = 5
PADX = 10
PADX_RIGHT = 10, 5
PADX_LEFT = 5, 10
PADX_MIDDLE = 0
