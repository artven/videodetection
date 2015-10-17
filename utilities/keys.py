__author__ = 'rafal'

import cv2


def keypressed(key='q', delay=1):
    pressed = cv2.waitKey(delay) & 0xFF
    return pressed == ord(key)