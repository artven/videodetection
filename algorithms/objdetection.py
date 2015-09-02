__author__ = 'rafal'

import cv2
import numpy as np
from utilities import keypressed


class ObjectDetector:

    @staticmethod
    def find(img):
        # Mark object, based on substracted image.
        height, width = img.shape
        size = img.size
        _, marked_image = cv2.connectedComponents(img)
        unique_markers = np.unique(marked_image)

        resultPoints = []

        for marker in unique_markers:
            markedRegion = np.uint8(marked_image == marker)
            # TODO zastosować klase CountourDetector
            image, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[0]
            leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
            rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
            topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
            bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
            pt1, pt2 = (leftmost[0], bottommost[1]), (rightmost[0], topmost[1])

            resultPoints.append((pt1, pt2))

        return resultPoints

    @staticmethod
    def mark(img, points):
        for point in points:
            cv2.rectangle(img, point[0], point[1], (0, 0, 255), thickness=2)

    @staticmethod
    def drawObjectsBorders(img):
        newImg = img.copy()
        objectPoints = ObjectDetector.find(newImg)
        newImg = cv2.cvtColor(newImg, cv2.COLOR_GRAY2BGR)
        ObjectDetector.mark(newImg, objectPoints)
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


