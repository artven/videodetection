__author__ = 'rafal'

import cv2
import numpy as np
from utilities import keypressed
from algorithms.contourdet import ContourDetector


class Obj:

    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2

    def update(self, obj):
        # Update object infromation from another object
        self.pt1 = obj.pt1
        self.pt2 = obj.pt2


class ObjectDetector:

    @staticmethod
    def find(img):
        # Find objects, based on substracted image.
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

            contours = ContourDetector.find(img)
            cnt = contours[0]
            leftmost, rightmost, topmost, bottommost = ContourDetector.extremePoints(cnt)
            pt1, pt2 = (leftmost[0], bottommost[1]), (rightmost[0], topmost[1])
            result.append(Obj(pt1, pt2))

        return result

    @staticmethod
    def mark(img, objects):
        for obj in objects:
            cv2.rectangle(img, obj.pt1, obj.pt2, (0, 0, 255), thickness=2)

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


