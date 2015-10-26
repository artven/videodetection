__author__ = 'rafal'

import os
import cv2

def clear_console():
    os.system('clear')

def key_pressed(key='q', delay=1):
    pressed = cv2.waitKey(delay) & 0xFF
    return pressed == ord(key)

def convertGray2BGR(grayFrame):
    return cv2.cvtColor(grayFrame, cv2.COLOR_GRAY2BGR)


def convertBGR2Gray(bgrFrame):
    return cv2.cvtColor(bgrFrame, cv2.COLOR_BGR2GRAY)

