__author__ = 'rafal'

import cv2
import numpy as np

from algorithm.objects import Vehicle
from algorithm.contourdet import ContourDetector


class Detector:
    # Klasa dokonująca wtępnej selekcji obiektów.

    # Obiekty o mniejszej liczbie pixeli będą ignorowane.
    _pixelLimit = 1000

    @staticmethod
    def find(image):
        """ Oznacza potencjalne obiekty mogące być pojazdami. """

        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        result = []
        markedImage = Detector._markComponents(image)
        values = Detector._findValues(markedImage)

        for value in values:
            if not Detector._isBackground(value):
                markedRegion = Detector._getRegion(markedImage, value)
                if Detector._isBigEnough(markedRegion):
                    x, y, w, h = Detector._getSize(markedRegion)
                    result.append(Vehicle(x, y, w, h))

        return result

    @staticmethod
    def _markComponents(image):
        """ Oznacza niezależne obszary. """
        _, marked = cv2.connectedComponents(image)
        return marked

    @staticmethod
    def _findValues(image):
        """ Zwraca wszystkie wartości znajdujące się w obrazie. """
        return np.unique(image)

    @staticmethod
    def _isBackground(value):
        """ Sprawdza czy podana wartość oznacza tło. """
        return value == 0

    @staticmethod
    def _isBigEnough(region):
        """ Sprawdza czy obszar jest wystraczająco duży, aby być wartym rozważenia. """
        return np.count_nonzero(region) >= Detector._pixelLimit

    @staticmethod
    def _getRegion(img, value):
        """ Oznacza fragment obrazu mający podaną wartość. """
        return np.uint8(img == value)

    @staticmethod
    def _getSize(region):
        """ Zwraca lewy górny punkt regionu, oraz szerokość i wysokość obszaru. """
        contours = ContourDetector.find(region)
        cnt = contours[0]
        leftmost, rightmost, topmost, bottommost = ContourDetector.extremePoints(cnt)
        x = leftmost[0]
        y = topmost[1]
        w = abs(leftmost[0]-rightmost[0])
        h = abs(topmost[1] - bottommost[1])
        return x, y, w, h



