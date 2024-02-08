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
ERR_COLOR_LIGHT = "#DD0015"
ERR_COLOR = "#880015"
ERR_COLOR_HOVER = "#6E0011"
DISABLED_COLOR = "#555555"
WARNING_COLOR = "#FFC000"
WARNING_COLOR_HOVER = "#C09200"

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
exposure_option = Literal["short", "long"]
class_option = Literal[
    "manual", "semi", "auto", "serial", "gui", "smart", "mu0", "mcu0", "control"
]
level_option = Literal["info", "error", "warning", "success"]
control_option = Literal["start", "pause", "stop", "continuos", "expand"]
aux_option = Literal["enable", "hlv", "mag", "select", "calib", "fpd"]
dur_option = Literal["short", "long"]
mode_option = Literal["mA", "FPD", "manual", "auto"]
ok_option = Literal["on", "off"]

all_calibrations = Literal[
    "offset",
    "defect",
    "defect_solid",
    "pixel_defect",
    "shading",
    "uniformity",
    
    "defect_solid_stereo",
    "defect_solid_biopsy",
    "defect_solid_tomo",
    "uniformity_stereo",
    "uniformity_biopsy",
    "uniformity_tomo",
    "uniformity_es",
]

BASIC_CALIBRATIONS: list[all_calibrations] = [
    "offset",
    "defect",
    "defect_solid",
    "pixel_defect",
    "shading",
    "uniformity",
]
TOMO_CALIBRATIONS: list[all_calibrations] = [
    "offset",
    "defect",
    "defect_solid",
    "pixel_defect",
    "shading",
    "uniformity",
    "defect_solid_tomo",
    "uniformity_tomo",
]
FULL_CALIBRATIONS: list[all_calibrations] = [
    "offset",
    "defect",
    "defect_solid",
    "pixel_defect",
    "shading",
    "uniformity",
    "defect_solid_stereo",
    "defect_solid_biopsy",
    "defect_solid_tomo",
    "uniformity_stereo",
    "uniformity_biopsy",
    "uniformity_tomo",
]
ALL_CALIBRATIONS: list[all_calibrations] = [
    "offset",
    "defect",
    "defect_solid",
    "pixel_defect",
    "shading",
    "uniformity",
    "defect_solid_stereo",
    "defect_solid_biopsy",
    "defect_solid_tomo",
    "uniformity_stereo",
    "uniformity_biopsy",
    "uniformity_tomo",
    "uniformity_es",
]

PADY_FRAME = 10, 0
PADY_END = 10
PADX_INSIDE_FRAME = 10
PADY_INSIDE_FRAME = (5, 0)
PADY_INSIDE_LAST = 5
PADX = 10
PADX_RIGHT = 10, 5
PADX_LEFT = 5, 10
PADX_MIDDLE = 0
