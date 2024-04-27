from ComputerVision.ComputerVision import ComputerVision
from ComputerVision.cv_types import *
import os

cv = ComputerVision(monitor="3M")
os.system("cls")


def check_status():
    status: list[status_mu] = ["blocked"]

    for i in range(100, 80, -5):
        confidence = i / 100
        isFound = False
        for state in status:
            x, _ = cv.get_status(state, confidence)
            if x > 0:
                print(f"{state} found c: {confidence}")
                isFound = True
                break
        if isFound:
            break

    status: list[status_mu] = ["exposure"]

    for i in range(100, 80, -5):
        confidence = i / 100
        isFound = False
        for state in status:
            x, _ = cv.get_status(state, confidence)
            if x > 0:
                print(f"{state} found c: {confidence}")
                isFound = True
                break
        if isFound:
            break

    status: list[status_mu] = ["standby"]

    for i in range(70, 80, -5):
        confidence = i / 100
        isFound = False
        for state in status:
            x, _ = cv.get_status(state, confidence)
            if x > 0:
                print(f"{state} found c: {confidence}")
                isFound = True
                break
        if isFound:
            break


def check_button_mcu_mutl():
    icons: list[mcu] = [
        "offset",
        "defect",
        "defect_solid",
        "pixel_defect",
        "shading",
        "uniformity",
    ]

    for i in range(100, 80, -5):
        confidence = i / 100
        count = 0
        for icon in icons:
            x, _ = cv.get_icon_coords(icon, confidence)
            if x > 0:
                print(f"{icon} found c: {confidence}")
                count += 1
        print("c: ", confidence, "matches: ", count, "\n")


def check_aws():
    icons: list[aws] = ["calib", "field_calibration", "ok", "ok2"]

    for i in range(100, 80, -5):
        confidence = i / 100
        isFound = False
        for icon in icons:
            x, _ = cv.get_icon_coords(icon, confidence)
            if x > 0:
                print(f"{icon} found c: {confidence}")
                isFound = True
                break
        if isFound:
            break


def check_mcu_tabs():
    icons: list[mcu_tabs] = ["cal_selected", "cal_opt_selected", "mcua", "mcub"]

    for i in range(100, 80, -5):
        confidence = i / 100
        count = 0
        for icon in icons:
            x, _ = cv.get_icon_coords(icon, confidence)
            if x > 0:
                print(f"{icon} found c: {confidence}")
                count += 1
        print("c: ", confidence, "matches: ", count, "\n")


check_mcu_tabs()
