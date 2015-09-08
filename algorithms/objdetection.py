__author__ = 'rafal'

import cv2
import numpy as np
from utilities import keypressed
from algorithms.contourdet import ContourDetector


class Obj:

    NewObj = 0
    Followed = 1
    Unknow = 2

    def __init__(self, pt1, pt2, status=0):
        self._pt1 = pt1  # (leftmost, bottommost)
        self._pt2 = pt2  # (rightmost, topmost)
        self._status = Obj.NewObj
        self._timeFollowed = 0
        self._timeUnknow = 0


    def __eq__(self, other):
        pass

    def update(self, obj):
        pass

    # getters
    def getPt1(self):
        # returns (leftmost, bottommost) point
        return self._pt1

    def getPt2(self):
        # returns (rightmost, topmost) point
        return self._pt2

    def getStatus(self):
        return self._status

    def getRectangle(self):
        x = self._pt1[0]  # leftmost
        y = self._pt2[1]  # topmost
        w = abs(self._pt1[0] - self._pt1[0])  # |leftmost - topmost|
        h = abs(self._pt1[1] - self._pt1[1])  # |topmost - bottommost|
        return x, y, w, h








class ObjectDetector:

    @staticmethod
    def find(img):
        # Find objects, based on substracted image.
        # Returns tuple of found objects.
        _, marked_image = cv2.connectedComponents(img)
        unique_markers = np.unique(marked_image)

        result = []
        for marker in unique_markers:

            # Avoid 0-marked region
            if marker == 0:
                continue

            markedRegion = np.uint8(marked_image == marker)

            # Check if new region is not too small
            if np.count_nonzero(markedRegion) < 500:  # TODO zmienić na % obrazu
                continue

            contours = ContourDetector.find(markedRegion)
            cnt = contours[0]
            leftmost, rightmost, topmost, bottommost = ContourDetector.extremePoints(cnt)
            pt1, pt2 = (leftmost[0], bottommost[1]), (rightmost[0], topmost[1])
            result.append(Obj(pt1, pt2))

        return result

    @staticmethod
    def mark(img, objects):
        markedImage = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) if len(img.shape) == 2 else img.copy()
        for obj in objects:
            cv2.rectangle(markedImage, obj.getPt1(), obj.getPt2(), (0, 0, 255), thickness=4)
        return markedImage

    @staticmethod
    def drawObjectsBorders(img):
        newImg = img.copy()
        objects = ObjectDetector.find(newImg)
        newImg = cv2.cvtColor(newImg, cv2.COLOR_GRAY2BGR)
        ObjectDetector.mark(newImg, objects)
        return newImg


if __name__ == "__main__":

    img = np.zeros([400, 400], dtype=np.uint8)
    val = 255
    img[100:300, 50:150] = val
    img[350:380, 60:150] = val

    winname = "output window"
    cv2.namedWindow(winname, cv2.WINDOW_FREERATIO)
    markedImg = ObjectDetector.drawObjectsBorders(img)


    while not keypressed():
        cv2.imshow(winname, markedImg)

cv2.destroyAllWindows()


