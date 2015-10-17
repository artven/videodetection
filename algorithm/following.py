__author__ = 'rafal'

import cv2
import numpy as np

from algorithm.objects import Vehicle

# from algorithm.contourdet import ContourDetector


class Follower:
    tracked = []
    unknown = []

    # liczba klatek przez jakie obiekt może pozostawać nieznanymi
    timeUnknowLimit = 10

    @staticmethod
    def update(newVehicles):

        found = []

        # dokonaj aktualizacji czasu pozostawania śledzonym obiektem
        for veh in Follower.tracked:
            veh.updateTimes()

        # dokonaj aktualizacji czasu pozostawania nieznanym obiektem
        for veh in Follower.unknown:
            veh.updateTimes()

        # usuń elementy pozostałe zbyt długo nieznanymi
        for veh in Follower.unknown:
            if veh.getTimeUnknow() > Follower.timeUnknowLimit:
                Follower.unknown.remove(veh)

        # spróbuj dopasować obecnie śledzone pojazdy do nowych obiektów
        # dopasowany obiekt dodaj do znalezionych
        for currentvehicle in Follower.tracked:
            for newvehicle in newVehicles:
                if Follower.__areConnected(currentvehicle, newvehicle):
                    foundvehicle = Follower.__makeTrackedVehicle(currentvehicle, newvehicle)
                    found.append(foundvehicle)
                    # WTF
                    if currentvehicle in Follower.tracked:
                        Follower.tracked.remove(currentvehicle)
                    newVehicles.remove(newvehicle)

        # spróbuj dopasować nieznane pojazdy do nowych obiektów
        # dopasowany obiekt dodaj do znalezionych
        for unkvehicle in Follower.unknown:
            for newvehicle in newVehicles:
                if Follower.__areConnected(unkvehicle, newvehicle):
                    foundvehicle = Follower.__makeTrackedVehicle(unkvehicle, newvehicle)
                    found.append(foundvehicle)
                    if unkvehicle in Follower.unknown:
                        Follower.unknown.remove(unkvehicle)
                    newVehicles.remove(newvehicle)

        # niedopasowane nowe obiekty dodaj do nieznanych
        for veh in newVehicles:
            Follower.unknown.append(veh)

        # obiekty śledzone bez następców dodaj do nieznanych
        for veh in Follower.tracked:
            Follower.unknown.append(veh)
            Follower.tracked.remove(veh)

        # obiekty znalezione dodaj do śledzonych
        for veh in found:
            Follower.tracked.append(veh)
            found.remove(veh)

        return Follower.tracked

    @staticmethod
    def __areConnected(vehicle1, vehicle2):
        """ Sprawdza czy dwa pojazdy mogą być ze sobą powiązane. """
        x1, y1, w1, h1 = vehicle1.getCoordinates()
        x2, y2, w2, h2 = vehicle2.getCoordinates()

        return ((x2 <= x1 + w1) if (x1 < x2) else (x1 <= x2 + w2)) and \
               ((y2 <= y1 + h1) if (y1 < y2) else (y1 <= y2 + h2))

    @staticmethod
    def __makeTrackedVehicle(currentvehicle, newvehicle):
        """ Tworzy wspólny obiekt z pozjazdów z poprzedniej i nowej klatki. """

        x1, y1, w1, h1 = currentvehicle.getCoordinates()
        x2, y2, w2, h2 = newvehicle.getCoordinates()

        # wyliczenie nowych wymiarów obiektu
        w = int((w1+w2)/2)
        h = int((h1+h2)/2)

        # wyliczenie prędkości
        pixelDiff = x2 - x1

        trackedvehicle = Vehicle(x2, y2, (w1+w2)/2, (h1+h2)/2, Vehicle.STATUS_TRACKED, pixelDiff=pixelDiff)
        return trackedvehicle


"""

    @staticmethod
    def connectionRatio(oldobj, newobj):
        # Calculates area of common part
        x1, y1, w1, h1 = oldobj.getRectangle()
        x2, y2, w2, h2 = newobj.getRectangle()
        tmpWidth = max(x1+w1, x2+w2) + 1    # +1 added for including borders
        tmpHeight = max(y1+h1, y2+h2) + 1

        oldObjArea = w1 * h1  # Calculate area of old object

        # Mark both areas on image
        tmp = np.zeros([tmpHeight, tmpWidth], dtype=np.uint8)
        tmp[y1:(y1+h1+1), x1:(x1+w1+1)] += 1
        tmp[y2:(y2+h2+1), x2:(x2+w2+1)] += 1

        commonPart = np.uint8(tmp == 2)  # Find common part
        contours = ContourDetector.find(commonPart)
        cnt = contours[0]
        leftmost, rightmost, topmost, bottommost = ContourDetector.extremePoints(cnt)
        w = abs(leftmost[0] - rightmost[0])
        h = abs(topmost[1] - bottommost[1])
        commonPartArea = w * h

        return (commonPartArea / oldObjArea) * 100
"""


