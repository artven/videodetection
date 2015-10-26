__author__ = 'rafal'

import cv2
import numpy as np

from src.objects import Vehicle
from src.contour import ContourDetector
from src.objects import Frame

class Detector:
    # Klasa dokonująca wtępnej selekcji obiektów.

    # Właściwości klasy.
    # Obiekty o mniejszej liczbie pixeli będą ignorowane.
    pixelLimit = 1000
    # Granica ignorowania w poziomie.
    verticalBorder = 200
    # Granica ignorowania w pionie.
    horizontalBorder = 50

    # Interfejs klasy.
    @staticmethod
    def find(image):
        """
        Oznacza potencjalne obiekty mogące być pojazdami.
        :param image:
        :return:
        """

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
    def select(vehicles, frame: Frame, ):
        """
        Dokonuje selekcji znalezionych obiektów. Odrzuca obiekty znajdujące się przy krawędzi obrazu.
        :return: Lista pojazdów
        """

        height, width = frame.getSize()
        result = []
        for vehic in vehicles:
            if (vehic.centerx > border) and (vehic.centerx < width-border) and (vehic.centery>horizontalborder) and \
                (vehic.centery < height-horizontalborder):
                result.append(vehic)
        return result

    def drawDetectionRegion(self, frame):
        leftUpperPoint = (border, horizontalborder)
        rightUpperPoint = (width-border, horizontalborder)
        leftLowerPoint = (border, height-horizontalborder)
        rightLowerPoint = (width-border, height-horizontalborder)
        frame.img = cv2.line(frame.img, leftLowerPoint, leftUpperPoint, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, leftLowerPoint, rightLowerPoint, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, rightLowerPoint, rightUpperPoint, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, leftUpperPoint, rightUpperPoint, (0, 0, 255), thickness=3)

    # Funkcje pomocnicze.
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
        return np.count_nonzero(region) >= Detector.pixelLimit

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



