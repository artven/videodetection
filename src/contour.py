__author__ = 'rafal'

import cv2

# TODO dopisać komenatze
class ContourDetector:

    @staticmethod
    def find(frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE):
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

        M = ContourDetector.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
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
