import mss
import pyautogui

import cv2 as cv
import numpy as np

with mss.mss() as sct:
    screen = sct.grab(sct.monitors[1])
    screen = np.array(screen)  # Convert to NumPy array
    screen = cv.cvtColor(screen, cv.COLOR_RGB2BGR)  # Convert RGB to BGR color

    icon = cv.imread("img/status_mu/standby.png", cv.COLOR_RGB2BGR)

    # cv.imshow("Computer Vision", screen)
    # cv.imshow("icon", icon)

    result = cv.matchTemplate(screen, icon, cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print(min_loc, max_loc)

    w = icon.shape[1]
    h = icon.shape[0]

    threshold = .68
    yloc, xloc = np.where(result >= threshold)

    for (x, y) in zip(xloc, yloc):
        cv.rectangle(screen, (x, y), (x + w, y + h), (0,255,255), 2)
    cv.imshow("Computer Vision", screen)
    cv.waitKey()
    cv.destroyAllWindows()
