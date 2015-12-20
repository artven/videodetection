# -*- coding: utf8 -*-
__author__ = "rafal"
__doc__ = "Moduł odpowiedzialny za detekcję obiektów."

import cv2
import numpy as np

try:
    from src.video import Frame
    from src.config import Configuration
except ImportError:
    from video import Frame
    from config import Configuration


class Vehicle:
    """
    Klasa opisująca pojazd.
    """

    def __init__(self, x, y, w, h):
        """

        :param x: Współrzędna x-owa lewego-górnego wierzchoła.
        :param y: Współrzędna y-owa lewego-górnego wierzchoła.
        :param w: Długość pojazdu.
        :param h: Wysokość pojazdu.
        """

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
        """
        Zwraca współrzędne opisujące pojazd.

        :return: Współrzędne x, y, szerokość, wysokość.
        :rtype: tuple
        """

        return int(self.x), int(self.y), int(self.w), int(self.h)

# TODO zmienić na rysowanie pojedynczego samochodu
def draw_vehicles(frame: Frame, vehicles: list):
    """
    Oznacza na obrazie pojazdy wraz ze środkami ciężkości.

    :param Frame frame: Klatka obrazu.
    :param list vehicles: Lista pojazdów.
    :return: Obraz z oznaczonymi pojazdami.
    :rtype: numpy.array
    """

    for veh in vehicles:
        x, y, w, h = veh.get_coordinates()
        cx = veh.centerx
        cy = veh.centery
        frame.img = cv2.rectangle(frame.img, (x, y), (x+w, y+h), (0, 255, 0), thickness=4)
        frame.img = cv2.line(frame.img, (cx, cy-10), (cx, cy+10), (0, 255, 0), thickness=4)
        frame.img = cv2.line(frame.img, (cx-10, cy), (cx+10, cy), (0, 255, 0), thickness=4)
    return frame


class Detector:
    """
    Klasa dokonująca wtępnej selekcji obiektów.
    """

    # Interfejs klasy.
    @staticmethod
    def find_vehicles(frame: Frame):
        """
        Znajduje pojazdy na obrazie.

        :param Frame frame: Klatka obrazu.
        :return: Znlezione pojazdy, maska binarna.
        :rtype: list, np.ndarray
        """

        image = frame.img
        mask = Subtractor.apply(image)
        vehicles = Detector.__find_possible_vehicles(mask)
        selected_vehicles = Detector.__select(vehicles, frame)
        return selected_vehicles, mask

    @staticmethod
    def __find_possible_vehicles(bin_image: np.ndarray):
        """
        Oznacza potencjalne obiekty mogące być pojazdami.

        :param np.ndarray bin_image: Binarna maska obrazu.
        :return: Wektor obiektów mogących być pojazdami.
        :rtype: list
        """

        if len(bin_image.shape) == 3:
            bin_image = cv2.cvtColor(bin_image, cv2.COLOR_BGR2GRAY)

        result = []
        marked_image = Detector.__mark_components(bin_image)
        values = Detector.__find_unique_values(marked_image)

        for value in values:
            if not Detector.__is_background(value):
                marked_region = Detector.__get_region(marked_image, value)
                if Detector.__has_valid_size(marked_region):
                    x, y, w, h = Detector.__get_size(marked_region)
                    result.append(Vehicle(x, y, w, h))

        return result

    @staticmethod
    def __select(vehicles: list, frame: Frame):
        """
        Dokonuje selekcji znalezionych obiektów. Odrzuca obiekty znajdujące się przy krawędzi obrazu.

        :param list vehicles: Wektor potencjalnych samochodów.
        :param Frame frame: Klatka obrazu
        :return: Wyseleksjonowane pojazdy.
        :rtype:  list
        """

        height, width = frame.size()
        result = []
        for vehic in vehicles:
            horizontal_border = Configuration.horizontal_border()
            vertical_border = Configuration.vertical_border()
            if (vehic.centerx > horizontal_border) and (vehic.centerx < width-horizontal_border)\
                    and (vehic.centery > vertical_border) and (vehic.centery < height-vertical_border):
                result.append(vehic)
        return result

    @staticmethod
    def draw_detection_region(frame: Frame):
        """
        Rysuje na klatce obszar czułości kamery.

        :param Frame frame: Klatka obrazu.
        :return: Klatka obrazu z oznaczonym obszarem.
        :rtype: Frame
        """

        height, width = frame.size()
        horizontal_border = Configuration.horizontal_border()
        vertical_border = Configuration.vertical_border()
        lup = (int(horizontal_border), int(vertical_border))
        rup = (int(width-horizontal_border), int(vertical_border))
        llp = (int(horizontal_border), int(height-vertical_border))
        rlp = (int(width-horizontal_border), int(height-vertical_border))
        frame.img = cv2.line(frame.img, llp, lup, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, llp, rlp, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, rlp, rup, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, lup, rup, (0, 0, 255), thickness=3)

        return frame

    # Funkcje pomocnicze.
    @staticmethod
    def __mark_components(image: np.ndarray):
        """
        Oznacza niezależne obszary.

        :param np.ndarray image: Obraz.
        :return: Obraz z wyróżnionymi rozłącznymi obszarami.
        :rtype: np.ndarray
        """

        _, marked = cv2.connectedComponents(image)
        return marked

    @staticmethod
    def __find_unique_values(image: np.ndarray):
        """
        Znajduje unikalne wartości na obrazie.

        :param np.ndarray image: Obraz z oznaczonymi obszarami.
        :return: Lista wartości.
        :rtype: list
        """

        return np.unique(image)

    @staticmethod
    def __is_background(value: int):
        """
        Sprawdza czy podana wartość oznacza tło.

        :param int value: Sprawdzana wartość.
        :return: Prawda/fałsz.
        :rtype: bool
        """

        return value == 0

    @staticmethod
    def __has_valid_size(region: np.ndarray):
        """
        Sprawdza czy obszar nie jest za mały oraz za duży.

        :param np.ndarray region: Obraz zwierający region oznaczony niezerową wartością.
        :return: Prawda/fałsz.
        :rtype: bool
        """

        # TODO dodać to do konfiguracji
        max = (480*720/2)
        min = Configuration.pixel_limit()
        return (np.count_nonzero(region) >= min) and (np.count_nonzero(region) < max)

    @staticmethod
    def __get_region(img: np.ndarray, value: int):
        """
        Oznacza fragment obrazu mający podaną wartość.

        :param np.ndarray img: Obraz.
        :param int value: Wartość.
        :return: Oznaczony obraz.
        :rtype: np.ndarray
        """

        return np.uint8(img == value)

    @staticmethod
    def __get_size(region: np.ndarray):
        """
        Zwraca lewy górny punkt regionu, oraz szerokość i wysokość obszaru.

        :param np.ndarray region: Wycinek obrazu binarnego.
        :return: Punkty opisujące obszar.
        :rtype: tuple
        """

        contours = ContourDetector.find(region)
        cnt = contours[0]
        leftmost, rightmost, topmost, bottommost = ContourDetector.extreme_points(cnt)
        x = leftmost[0]
        y = topmost[1]
        w = abs(leftmost[0]-rightmost[0])
        h = abs(topmost[1] - bottommost[1])
        return x, y, w, h


class Subtractor:
    """
    Klasa wyodrębniająca tło.
    """

    # Silnik wyodrębniania tła.
    substractor_engine = cv2.createBackgroundSubtractorMOG2()

    # Parametry filtracji obrazu.
    __operation = cv2.MORPH_OPEN
    __kernel = cv2.MORPH_ELLIPSE
    __kernelsize = (3, 3)
    __mediansize = 5
    __dilateiter = 5

    @staticmethod
    def apply(image: np.ndarray):
        """
        Dokonuje wyodrębnienia tła z klatki obrazu. Zwraca zbinearyzowany obraz.

        :param np.ndarray image: Obraz.
        :return: Oznaczony obraz.
        :rtype: np.ndarray
        """

        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        substracted_frame = Subtractor.substractor_engine.apply(image)
        filtered_frame = Subtractor.__filter(substracted_frame)
        _, substracted = cv2.threshold(filtered_frame, 0, 255, cv2.THRESH_BINARY)
        return substracted

    @staticmethod
    def __filter(image: np.ndarray):
        """
        Dokonuje filtracji za pomocą mediany i dylatacji.

        :param image: Binarny obraz wejściowy.
        :return: Wynikowy przefiltrowany obraz.
        :rtype: np.ndarray
        """

        ker = cv2.getStructuringElement(Subtractor.__kernel, Subtractor.__kernelsize)
        morphframe = cv2.morphologyEx(image, Subtractor.__operation, ker)
        medianframe = cv2.medianBlur(morphframe, Subtractor.__mediansize)
        dilatframe = cv2.dilate(medianframe, ker, iterations=Subtractor.__dilateiter)
        return dilatframe


class ContourDetector:

    @staticmethod
    def find(frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE):
        """
        Wyszukuje kontury na obrazie.

        :param frame:
        :param mode:
        :param method: Metoda aproksymacji lini konturu.
        :return: Tablica konturów.
        """

        img, contours, hierarchy = cv2.findContours(frame.copy(), mode, method)
        return contours

    @staticmethod
    def extreme_points(cnt):
        """
        Zwraca graniczne punkty obszaru objęego konturem.

        :param cnt: Kontur z hierarchi.
        :return: Graniczne punkty: lewy, prawy, górny, dolny.
        """

        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
        return leftmost, rightmost, topmost, bottommost

    @staticmethod
    def draw(img, cnt, color=(0, 255, 0), thickness=1):
        """
        Rysuje kontur na obrazie.

        :param img: Obraz wejściowy.
        :param cnt: Kontur z hierarchi.
        :param color: Kolor konturu, domyślnie zielony.
        :param thickness: Grubość lini.
        :return: Obraz z oznaczonym konturem.
        """

        result = img.copy()
        cv2.drawContours(result, [cnt], 0, color, thickness)
        return result

    @staticmethod
    def moments(cnt):
        """
        Oblicza momenty obszaru objętego konturem.

        :param cnt: Kontur z hierarchi.
        :return:  Momenty konturu.
        """

        return cv2.moments(cnt)

    @staticmethod
    def centroid(cnt):
        """
        Wyznacz środek obszaru objętego konturem.

        :param cnt: Kontur z hierarchi.
        :return: Współrzędne środka: x, y.
        """

        moment = ContourDetector.moments(cnt)
        cx = int(moment['m10']/moment['m00'])
        cy = int(moment['m01']/moment['m00'])
        return cx, cy

    @staticmethod
    def area(cnt):
        """
        Oblicza pole konturu.

        :param cnt: Kontur z hierarchi.
        :return: Pole konturu.
        """

        return cv2.contourArea(cnt)

    @staticmethod
    def bounding_rectangle(cnt):
        """
        Zwraca parametry prostokąta pokrywającego kontur.

        :param cnt: Kontur z hierarchi.
        :return: Opis prostokąta: wierzchołek(x, y), szerokość, wysokość.
        """

        x, y, w, h = cv2.boundingRect(cnt)
        return x, y, w, h