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


def draw_vehicles(frame, vehicles):
    for veh in vehicles:
        x, y, w, h = veh.get_coordinates()
        cx = veh.centerx
        cy = veh.centery
        frame.img = cv2.rectangle(frame.img, (x, y), (x+w, y+h), (0, 255, 0), thickness=4)
        frame.img = cv2.line(frame.img, (cx, cy-10), (cx, cy+10), (0, 255, 0), thickness=4)
        frame.img = cv2.line(frame.img, (cx-10, cy), (cx+10, cy), (0, 255, 0), thickness=4)
    return frame


class Detector:
    # Klasa dokonująca wtępnej selekcji obiektów.

    # Właściwości klasy.
    # Obiekty o mniejszej liczbie pixeli będą ignorowane.
    pixel_limit = 1000
    # Granica ignorowania w poziomie.
    horizontal_border = 200
    # Granica ignorowania w pionie.
    vertical_border = 50

    # Interfejs klasy.
    @staticmethod
    def find_vehicles(frame):
        image = frame.img
        mask = Subtractor.apply(image)
        vehicles = Detector.__find_possible_vehicles(mask)
        selected_vehicles = Detector.__select(vehicles, frame)
        return selected_vehicles, mask

    @staticmethod
    def __find_possible_vehicles(bin_image):
        """
        Oznacza potencjalne obiekty mogące być pojazdami.
        :param bin_image:
        :return:
        """

        if len(bin_image.shape) == 3:
            bin_image = cv2.cvtColor(bin_image, cv2.COLOR_BGR2GRAY)

        result = []
        markedImage = Detector.__mark_components(bin_image)
        values = Detector.__find_unique_values(markedImage)

        for value in values:
            if not Detector.__is_background(value):
                markedRegion = Detector.__get_region(markedImage, value)
                if Detector.__is_big_enough(markedRegion):
                    x, y, w, h = Detector.__get_size(markedRegion)
                    result.append(Vehicle(x, y, w, h))

        return result

    @staticmethod
    def __select(vehicles, frame: Frame):
        """
        Dokonuje selekcji znalezionych obiektów.
        Odrzuca obiekty znajdujące się przy krawędzi obrazu.
        :return: Lista pojazdów.
        """

        height, width = frame.size()
        result = []
        for vehic in vehicles:
            if (vehic.centerx > Detector.horizontal_border) and (vehic.centerx < width-Detector.horizontal_border)\
                    and (vehic.centery > Detector.vertical_border) and (vehic.centery < height-Detector.vertical_border):
                result.append(vehic)
        return result

    @staticmethod
    def draw_detection_region(frame):
        height, width = frame.size()
        lup = (Detector.horizontal_border, Detector.vertical_border)
        rup = (width-Detector.horizontal_border, Detector.vertical_border)
        llp = (Detector.horizontal_border, height-Detector.vertical_border)
        rlp = (width-Detector.horizontal_border, height-Detector.vertical_border)
        frame.img = cv2.line(frame.img, llp, lup, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, llp, rlp, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, rlp, rup, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, lup, rup, (0, 0, 255), thickness=3)

        return frame

    # Funkcje pomocnicze.
    @staticmethod
    def __mark_components(image):
        """ Oznacza niezależne obszary. """
        _, marked = cv2.connectedComponents(image)
        return marked

    @staticmethod
    def __find_unique_values(image):
        """ Zwraca wszystkie wartości znajdujące się w obrazie. """
        return np.unique(image)

    @staticmethod
    def __is_background(value):
        """ Sprawdza czy podana wartość oznacza tło. """
        return value == 0

    @staticmethod
    def __is_big_enough(region):
        """ Sprawdza czy obszar jest wystraczająco duży, aby być wartym rozważenia. """
        return np.count_nonzero(region) >= Detector.pixel_limit

    @staticmethod
    def __get_region(img, value):
        """ Oznacza fragment obrazu mający podaną wartość. """
        return np.uint8(img == value)

    @staticmethod
    def __get_size(region):
        """ Zwraca lewy górny punkt regionu, oraz szerokość i wysokość obszaru. """
        contours = ContourDetector.find(region)
        cnt = contours[0]
        leftmost, rightmost, topmost, bottommost = ContourDetector.extreme_points(cnt)
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

