__author__ = 'rafal'

import cv2

def keypressed(key='q', delay=5):
    return cv2.waitKey(delay) == ord(key)