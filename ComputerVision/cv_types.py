from typing import Literal

aws = Literal["calib", "field_calibration", "ok", "ok2"]
AWS: list[str] = ["calib", "field_calibration", "ok", "ok2"]
gen = Literal[
    "calibration_complete",
    "deviation",
    "exit_main",
    "exit_ma_calib",
    "gen_tools",
    "ma_calib",
]
GEN: list[str] = [
    "calibration_complete",
    "deviation",
    "exit_main",
    "exit_ma_calib",
    "gen_tools",
    "ma_calib",
]
mcu = Literal[
    "defect",
    "defect_solid",
    "offset",
    "pixel_defect",
    "sensitivity",
    "shading",
    "uniformity",
]
MCU: list[str] = [
    "defect",
    "defect_solid",
    "offset",
    "pixel_defect",
    "sensitivity",
    "shading",
    "uniformity",
]
mcu_opt = Literal[
    "defect_solid_biopsy",
    "defect_solid_stereo",
    "defect_solid_tomo",
    "uniformity_biopsy",
    "uniformity_es",
    "uniformity_stereo",
    "uniformity_tomo",
]
MCU_OPT: list[str] = [
    "defect_solid_biopsy",
    "defect_solid_stereo",
    "defect_solid_tomo",
    "uniformity_biopsy",
    "uniformity_es",
    "uniformity_stereo",
    "uniformity_tomo",
]
mcu_tabs = Literal["cal_opt_selected", "cal_selected", "mcua", "mcub", "mcuc"]
MCU_TABS: list[str] = ["cal_opt_selected", "cal_selected", "mcua", "mcub", "mcuc"]
mu = Literal["HVL", "MAG"]
MU: list[str] = ["HVL", "MAG"]
mutl = Literal["left_right", "only_left", "only_right"]
MUTL: list[str] = ["left_right", "only_left", "only_right"]
mu_gen = Literal["enable_ment"]
MU_GEN: list[str] = ["enable_ment"]
mu_tabs = Literal["calibration_selected", "generator_selected", "mua", "mub"]
MU_TABS: list[str] = ["calibration_selected", "generator_selected", "mua", "mub"]
ru = Literal["install", "MCU0", "MCU0_S", "MU0", "MU0_S", "mutl", "new"]
RU: list[str] = ["install", "MCU0", "MCU0_S", "MU0", "MU0_S", "mutl", "new"]
status_gen = Literal[
    "development", "exposing", "idle", "initializing", "push", "release"
]
STATUS_GEN: list[status_gen] = [
    "development",
    "exposing",
    "idle",
    "initializing",
    "push",
    "release",
]
status_mcu = Literal[
    "defect",
    "defect_solid",
    "exposure_required",
    "idle",
    "offline",
    "offset",
    "pasar",
    "pixel_defect",
    "saltar",
    "sensitivity",
    "shading",
    "uniformity",
]
STATUS_MCU: list[status_mcu] = [
    "defect",
    "defect_solid",
    "exposure_required",
    "idle",
    "offline",
    "offset",
    "pasar",
    "pixel_defect",
    "saltar",
    "sensitivity",
    "shading",
    "uniformity",
]
status_mu = Literal[
    "blocked",
    "blocked_text",
    "exposure",
    "offline",
    "prep_done_text",
    "standby",
    "standby_text",
]
STATUS_MU: list[status_mu] = [
    "blocked",
    "blocked_text",
    "exposure",
    "offline",
    "prep_done_text",
    "standby",
    "standby_text",
]
monitors = Literal["2M", "3M"]
keys = Literal[
    "aws",
    "gen",
    "mcu",
    "mcu_opt",
    "mcu_tabs",
    "mu",
    "mutl",
    "mu_gen",
    "mu_tabs",
    "ru",
    "status_gen",
    "status_mcu",
    "status_mu",
]
all_buttons = Literal[
    "calib",
    "field_calibration",
    "ok",
    "ok2",
    "calib",
    "field_calibration",
    "ok",
    "ok2",
    "calibration_complete",
    "deviation",
    "exit_main",
    "exit_ma_calib",
    "gen_tools",
    "ma_calib",
    "calibration_complete",
    "deviation",
    "exit_main",
    "exit_ma_calib",
    "gen_tools",
    "ma_calib",
    "defect",
    "defect_solid",
    "offset",
    "pixel_defect",
    "sensitivity",
    "shading",
    "uniformity",
    "defect",
    "defect_solid",
    "offset",
    "pixel_defect",
    "sensitivity",
    "shading",
    "uniformity",
    "defect_solid_biopsy",
    "defect_solid_stereo",
    "defect_solid_tomo",
    "uniformity_biopsy",
    "uniformity_es",
    "uniformity_stereo",
    "uniformity_tomo",
    "defect_solid_biopsy",
    "defect_solid_stereo",
    "defect_solid_tomo",
    "uniformity_biopsy",
    "uniformity_es",
    "uniformity_stereo",
    "uniformity_tomo",
    "cal_opt_selected",
    "cal_selected",
    "mcua",
    "mcub",
    "cal_opt_selected",
    "cal_selected",
    "mcua",
    "mcub",
    "mcuc",
    "HVL",
    "MAG",
    "HVL",
    "MAG",
    "left_right",
    "only_left",
    "only_right",
    "left_right",
    "only_left",
    "only_right",
    "enable_ment",
    "enable_ment",
    "calibration_selected",
    "generator_selected",
    "mua",
    "mub",
    "calibration_selected",
    "generator_selected",
    "mua",
    "mub",
    "install",
    "MCU0",
    "MCU0_S",
    "MU0",
    "MU0_S",
    "mutl",
    "new",
    "install",
    "MCU0",
    "MCU0_S",
    "MU0",
    "MU0_S",
    "mutl",
    "new",
    "development",
    "exposing",
    "idle",
    "initializing",
    "push",
    "release",
    "development",
    "exposing",
    "idle",
    "initializing",
    "push",
    "release",
    "defect",
    "defect_solid",
    "exposure_required",
    "idle",
    "offline",
    "offset",
    "pasar",
    "pixel_defect",
    "saltar",
    "sensitivity",
    "shading",
    "uniformity",
    "defect",
    "defect_solid",
    "exposure_required",
    "idle",
    "offline",
    "offset",
    "pasar",
    "pixel_defect",
    "saltar",
    "sensitivity",
    "shading",
    "uniformity",
    "blocked",
    "exposure",
    "offline",
    "standby",
    "blocked",
    "blocked_text",
    "exposure",
    "offline",
    "prep_done_text",
    "standby",
    "standby_text",
]
