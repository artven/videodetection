__author__ = 'rafal'

from algorithm.contourdet import ContourDetector
import cv2

class SizeMeasurment:
    # Klasa dokonująca pomiaru rozmiaru samochodu.

    # Odległość w pikselach.
    __pixelLength = 200

    # Odległość rzeczywista w metrach.
    __metersLength = 4

    # Interfejs klasy.

    @staticmethod
    def calculateWidth(car):
        width = car.w
        ratio = SizeMeasurment.__getRatio()
        return width * ratio

    @staticmethod
    def calculateHeight(car):
        height = car.h
        ratio = SizeMeasurment.__getRatio()
        return height * ratio

    @staticmethod
    def calculateArea(car, binaryMask):

        # Wyznacz rejon pojazdu na obrazie.
        x, y, w, h = car.getCoordinates()
        mask = binaryMask[y:y+h, x:x+w]

        # Znajdź kontury samochodu.
        contours = ContourDetector.find(mask)

        # Wyszkuaj kontur o największym polu.
        cnt = SizeMeasurment.__findBiggestContour(contours)

        # Oblicz pole konturu.
        area = ContourDetector.area(cnt)
        ratio = SizeMeasurment.__getRatio()
        area = round(area*ratio*ratio, 2)

        return area

    @staticmethod
    def drawSizeInfo(img, car, binaryMask, carWidth, carHeight, carArea):

        # Pobierz położenie pojazdu:
        x, y, w, h = car.getCoordinates()

        # Narysuj informacje o długości.
        pt1, pt2 = (x, y-20), (x+w, y-20)
        cv2.line(img, pt1, pt2, (255, 0, 0), thickness=2)

        # Narysuj informacje o wysokości.
        pt1, pt2 = (x-20, y), (x-20, y+h)
        cv2.line(img, pt1, pt2, (255, 0, 0), thickness=2)

        # Dorysuj "strzałki".
        pt1, pt2 = (x-25, y), (x-15, y)
        cv2.line(img, pt1, pt2, (255, 0, 0), thickness=2)
        pt1, pt2 = (x-25, y+h), (x-15, y+h)
        cv2.line(img, pt1, pt2, (255, 0, 0), thickness=2)
        pt1, pt2 = (x, y-15), (x, y-25)
        cv2.line(img, pt1, pt2, (255, 0, 0), thickness=2)
        pt1, pt2 = (x+w, y-15), (x+w, y-25)
        cv2.line(img, pt1, pt2, (255, 0, 0), thickness=2)

        # Dopisz tekst.
        text = "W:"+str(carWidth)+"m, H:"+str(carHeight)+"m, A:"+str(carArea)+"m2"
        org = (x, y-30)
        cv2.putText(img, text, org, cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0))

        return img

    # Funkcje pomocnicze.

    @staticmethod
    def __getRatio():
        meters = SizeMeasurment.__metersLength
        pixels = SizeMeasurment.__pixelLength
        ratio = float(meters) / pixels
        return ratio

    @staticmethod
    def __findBiggestContour(contours):
        if len(contours) > 1:
            maxArea, contourIndex = ContourDetector.area(contours[0]), 0
            for index in range(len(contours)):
                area = ContourDetector.area(contours[index])
                if area > maxArea:
                    maxArea, contourIndex = area, index
            cnt = contours[contourIndex]
            return cnt
        elif len(contours) == 1:
            return contours[0]  # TODO nie wiem czy ma być index
        else:
            return None

