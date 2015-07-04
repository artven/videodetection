__author__ = 'rafal'

import numpy as np
import cv2


class ContourDetector:

    def __init__(self):
        self.__image = None
        self.__contours = None
        self.__hierarchy = None
        self.__width = None
        self.__height = None

    def find(self, frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE):
        self.__height, self.__width = frame.shape
        _, self.__contours, self.__hierarchy = cv2.findContours(frame.copy(), mode, method)
        return self.__contours, self.__hierarchy

    def draw(self, cnt=-1, color=(0, 255, 0), thickness=1):

        result = np.zeros((self.__height, self.__width, 3), np.uint8)

        if cnt == -1:
            cv2.drawContours(result, self.__contours, -1, color, thickness)
        else:
            cnt = self.__contours[cnt]
            cv2.drawContours(result, [cnt], 0, color, thickness)

        return result

    def moments(self, cnt=0):
        cnt = self.__contours[cnt]
        return cv2.moments(cnt)

    def centroid(self, cnt=0):
        M = self.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx, cy

    def area(self, cnt=0):
        cnt = self.__contours[cnt]
        return cv2.contourArea(cnt)

    def perimeter(self, cnt=0, closed=True):
        cnt = self.__contours[cnt]
        return cv2.arcLength(cnt, closed)

    def approx(self, cnt=0, epsilon=0.1, closed=True):
        cnt = self.__contours[cnt]
        epsilon = epsilon*cv2.arcLength(cnt, closed)
        approx = cv2.approxPolyDP(cnt, epsilon, closed)
        return approx

    def convex_hull(self, cnt=0):
        cnt = self.__contours[cnt]
        hull = cv2.convexHull(cnt)
        return hull

    def is_convex(self, cnt=0):
        cnt = self.contour_count[cnt]
        return cv2.cv2.isContourConvex(cnt)

    def bounding_rectangle(self, cnt=0):
        x,y,w,h = cv2.boundingRect(cnt)
        return x,y,w,h

    def rotated_rectangle(self, cnt=0):
        cnt = self.contour_count[cnt]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        return box

    def circle(self, cnt=0):
        result = np.zeros((self.__height, self.__width, 3), np.uint8)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center, radius = (int(x), int(y)), int(radius)
        return center, radius

    @property
    def contour_count(self):
        return len(self.__contours) if self.__contours is not None else 0



if __name__ == "__main__":

    path = "../images/image_screenshot_04.07.2015.png"
    image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)

    window1 = "obraz wejsciowy"
    window2 = "kontury"
    cv2.namedWindow(window1)
    cv2.namedWindow(window2)

    cv2.imshow(window1, image)

    detector = ContourDetector()
    detector.find(image)
    cv2.imshow(window2, detector.draw())

    while 1:

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break