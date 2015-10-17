__author__ = 'rafal'

import numpy as np
import cv2


class ContourDetector:

    @staticmethod
    def find(frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE):
        img, contours, hierarchy = cv2.findContours(frame.copy(), mode, method)
        return contours

    @staticmethod
    def extremePoints(cnt):
        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
        return leftmost, rightmost, topmost, bottommost

    @staticmethod
    def draw(img, cnt, color=(0, 255, 0), thickness=1):
        result = img.copy()
        cv2.drawContours(result, [cnt], 0, color, thickness)
        return result

    @staticmethod
    def moments(cnt):
        return cv2.moments(cnt)

    @staticmethod
    def centroid(cnt):
        M = ContourDetector.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx, cy

    @staticmethod
    def area(cnt):
        return cv2.contourArea(cnt)

    @staticmethod
    def perimeter(cnt, closed=True):
        return cv2.arcLength(cnt, closed)

    @staticmethod
    def approx(cnt, epsilon=0.1, closed=True):
        epsilon = epsilon*cv2.arcLength(cnt, closed)
        approx = cv2.approxPolyDP(cnt, epsilon, closed)
        return approx

    @staticmethod
    def convexHull(cnt):
        return cv2.convexHull(cnt)

    @staticmethod
    def isConvex(cnt):
        return cv2.cv2.isContourConvex(cnt)

    @staticmethod
    def boundingRectangle(cnt):
        x, y, w, h = cv2.boundingRect(cnt)
        return x, y, w, h
