__author__ = 'rafal'

import cv2
import numpy as np

from utilities import keypressed
from algorithm.detection import Detector
from src.follow import Follower


if __name__ == "__main__":

    resultFrame = np.zeros([500, 500], dtype=np.uint8)

    regions = {1: (50, 200, 10, 80), 2: (100, 300, 50, 400)}
    foundObjects = []

    for value in regions.keys():
        cords = regions[value]
        tmp = np.zeros([500, 500], dtype=np.uint8)
        resultFrame[cords[0]:cords[1], cords[2]:cords[3]] = value
        tmp[cords[0]:cords[1], cords[2]:cords[3]] = value
        objs = Detector.find_possible_vehicles(np.uint8(tmp == value))
        foundObjects.extend(objs)

    # for obj in foundObjects:
    #    print(obj.getRectangle())

    resultFrame = Detector.mark(resultFrame, foundObjects)

    winname = "all regions"
    cv2.namedWindow(winname, cv2.WINDOW_FREERATIO)
    resultFrame[resultFrame != 0] = 255
    cv2.imshow(winname, resultFrame)

    if Follower.areConnected(foundObjects[0], foundObjects[1]):
        print("zachodzą na siebie!")
    else:
        print("są niezależne")

    print(Follower.connectionRatio(foundObjects[0], foundObjects[1]))


    while not keypressed():
        pass

    cv2.destroyAllWindows()
