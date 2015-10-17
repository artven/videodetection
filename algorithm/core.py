__author__ = 'rafal'

import cv2
import numpy as np

# główne składowe algorytmu
from algorithm.subtraction import Subtractor
from algorithm.detection import Detector
from algorithm.objects import drawObjects, Vehicle
from algorithm.following import Follower


def __convertGray2BGR(grayFrame):
    return cv2.cvtColor(grayFrame, cv2.COLOR_GRAY2BGR)


def __convertBGR2Gray(bgrFrame):
    return cv2.cvtColor(bgrFrame, cv2.COLOR_BGR2GRAY)


def algorithm(frame, width, height):
    result = np.zeros([2*height, 2*width, 3], dtype=np.uint8)

    # obraz orginalny
    result[:height, :width, :] = frame

    # wyodrębnianie tła
    substracted = Subtractor.apply(frame)
    _, substracted = cv2.threshold(substracted, 0, 255, cv2.THRESH_BINARY)
    result[:height, width:, :] = __convertGray2BGR(substracted)

    # wyszukiwanie obiektów na obrazie
    vehicles = Detector.find(substracted)
    result[height:, :width, :] = drawObjects(frame, vehicles, 4)

    # śledzenie pojazdów
    followedvehicles = Follower.update(vehicles)
    result[height:, width:, :] = drawObjects(frame, followedvehicles, 4)

    return result