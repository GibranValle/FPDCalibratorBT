from typing import Literal
aws = Literal['calib', 'field_calibration', 'ok', 'ok2']
gen = Literal['calibration_complete', 'deviation', 'exit_main', 'exit_ma_calib', 'gen_tools', 'ma_calib']
mcu = Literal['defect', 'defect_solid', 'offset', 'pixel_defect', 'sensitivity', 'shading', 'uniformity']
mcu_opt = Literal['defect_bpy', 'defect_stereo', 'defect_tomo', 'uniformity_bpy', 'uniformity_es', 'uniformity_stereo', 'uniformity_tomo']
mcu_tabs = Literal['cal_opt_selected', 'cal_selected', 'mcua', 'mcub']
mu = Literal['enable_ment', 'HVL', 'MAG']
mutl = Literal['left_right', 'only_left', 'only_right']
mu_tabs = Literal['calibration_selected', 'generator_selected', 'mua', 'mub']
ru = Literal['install', 'MCU0', 'MCU0_S', 'MU0', 'MU0_S', 'mutl', 'new']
status_gen = Literal['development', 'exposing', 'idle', 'initializing', 'push', 'release']
status_mcu = Literal['defect_solid', 'exposure_required', 'offline', 'offset', 'pasar', 'saltar', 'sensitivity', 'shading', 'uniformity']
status_mu = Literal['blocked', 'exposure', 'offline', 'standby']
keys = Literal['aws', 'gen', 'mcu', 'mcu_opt', 'mcu_tabs', 'mu', 'mutl', 'mu_tabs', 'ru', 'status_gen', 'status_mcu', 'status_mu']
