__author__ = 'rafal'

import cv2
import numpy as np
import time

from utilities.frame import Frame
from algorithm.objects import Vehicle

class VehiclesClassifier:

    # parametry pomiaru prędkości
    # odległość w pixelach pomiędzy granicami pomiaru
    pixelLength = 50
    # odległość w metrach pomiędzy granicami pomiaru
    metersLength = 1

    @staticmethod
    def performRating(vehiclesRecords):

        # sprawdź czy otrzymane rekordy nie są puste
        if vehiclesRecords is None or len(vehiclesRecords) == 0:
            return None

        result = []

        for record in vehiclesRecords:
            # dokonaj rozpakowania rekodru pojazdu
            newCar, frame, oldCar, oldframe, mask = record

            speed = VehiclesClassifier.calculateSpeed(newCar, frame, oldCar, oldframe)
            color = VehiclesClassifier.calculateColor(newCar, frame, mask)
            size = VehiclesClassifier.calculateSize(newCar, frame, mask)
            r = (speed, color, size)
            result.append(r)

        return result if len(result) else None

    @staticmethod
    def calculateSpeed(newCar, frame, oldCar, oldframe):
        return 2

    @staticmethod
    def calculateSize(newCar, frame, mask):
        return 1

    @staticmethod
    def calculateColor(newCar, frame, mask):
        return 0