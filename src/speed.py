__author__ = 'rafal'

import cv2

from src.objects import Vehicle
from utilities.frame import Frame


class SpeedMeasurment:
    # Klasa dokonująca pomiaru rozmiaru samochodu.

    # Odległość w pikselach.
    __pixelLength = 200

    # Odległość rzeczywista w metrach.
    __metersLength = 4

    # Interfejs klasy.

    @staticmethod
    def calculateSpeed(newCar: Vehicle, frame: Frame, oldCar: Vehicle, oldframe: Frame):

        timeDiff = None

        # Jeżeli ramka pochodzi z pliku wideo, różnica jest obliczana na podstawie jej numeru i fps-ów.
        if not frame.isFromCamera:
            frameCount = float(abs(frame.framePos - oldframe.framePos))
            timeDiff = frameCount * float(1/frame.fps)
        else:
            # Jeżeli ramka pochodzi z kamery, różnica jest obliczana na podstawie czasu jej pobrania.
            # TODO zrobić odejmowanie czasu
            pass

        pixelDiff = float(abs(newCar.centerx - oldCar.centerx))
        ratio = SpeedMeasurment.__getRatio()
        metersDiff = ratio * pixelDiff
        speed = round(metersDiff / timeDiff, 5) * 3.6

        return speed

    @staticmethod
    def drawSpeedInfo(car, speed, img):

        # Pobierz położenie pojazdu:
        x, y, w, h = car.getCoordinates()

        text = ("S: %.2f" % speed) + " km/h"
        org = (x, y+30)
        cv2.putText(img, text, org, cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0))
        return img

    # Funkcje pomocnicze.

    @staticmethod
    def __getRatio():
        meters = SpeedMeasurment.__metersLength
        pixels = SpeedMeasurment.__pixelLength
        ratio = float(meters) / pixels
        return ratio
