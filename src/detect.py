__author__ = 'rafal'

import cv2
import numpy as np

from src.contour import ContourDetector
from src.video import Frame


class Vehicle:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.centerx = x+int(w/2)
        self.centery = y+int(h/2)

    def __eq__(self, other):
        x, y, w, h = other.get_coordinates()
        return (self.__x, self.__y, self.__w, self.__h) == (x, y, w, h)

    def get_coordinates(self):
        """ Zwraca lewy-górny punkt oraz szerokość i wysokość """
        return int(self.x), int(self.y), int(self.w), int(self.h)



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
    def find_vehicle(frame):
        image = frame.img

        # Substrakcja tła
        bin_image = Subtractor.apply(image)
        vehicles = Detector.find_possible_vehicles(bin_image)
        Detector.select()


    @staticmethod
    def find_possible_vehicles(image):
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
        :return: Lista pojazdów.
        """

        height, width = frame.size()
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

    def algorithm(frame):
    # wyodrębnianie tła
    substracted = Subtractor.apply(frame.img)


    # wyszukiwanie obiektów na obrazie
    vehicles = Detector.find_possible_vehicles(substracted)

    return vehicles, substracted

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


class Subtractor:
    # Klasa wyodrębniająca tło oraz poruszające się elementy na obrazie.

    # Silnik wyodrębniania tła.
    substractor_engine = cv2.createBackgroundSubtractorMOG2()

    # Parametry filtracji obrazu.
    operation = cv2.MORPH_OPEN
    kernel = cv2.MORPH_ELLIPSE
    kernelsize = (3, 3)
    mediansize = 5
    dilateiter = 5

    @staticmethod
    def apply(image):
        """
        Dokonuje wyodrębnienia tła z klatki obrazu. Zwraca zbinearyzowany obraz.
        """

        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        substractedFrame = Subtractor.substractor_engine.apply(image)
        filteredFrame = Subtractor.__filter(substractedFrame)
        _, substracted = cv2.threshold(filteredFrame, 0, 255, cv2.THRESH_BINARY)
        return substracted

    @staticmethod
    def __filter(image):
        """
        Dokonuje filtracji za pomocą mediany i dylatacji.
        """
        ker = cv2.getStructuringElement(Subtractor.kernel, Subtractor.kernelsize)
        morphframe = cv2.morphologyEx(image, Subtractor.operation, ker)
        medianframe = cv2.medianBlur(morphframe, Subtractor.mediansize)
        dilatframe = cv2.dilate(medianframe, ker, iterations=Subtractor.dilateiter)
        return dilatframe

