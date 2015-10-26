__author__ = 'prusak smiec'

import cv2

# główne składowe algorytmu
from src.subtraction import Subtractor
from src.detect import Detector


def convertGray2BGR(grayFrame):
    return cv2.cvtColor(grayFrame, cv2.COLOR_GRAY2BGR)


def convertBGR2Gray(bgrFrame):
    return cv2.cvtColor(bgrFrame, cv2.COLOR_BGR2GRAY)


def algorithm(frame):
    # wyodrębnianie tła
    substracted = Subtractor.apply(frame.img)
    _, substracted = cv2.threshold(substracted, 0, 255, cv2.THRESH_BINARY)

    # wyszukiwanie obiektów na obrazie
    vehicles = Detector.find(substracted)

    return vehicles, substracted