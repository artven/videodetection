__author__ = 'rafal'

import cv2

class Vehicle:

    STATUS_NEW = 0
    STATUS_TRACKED = 1
    STATUS_UNKNOW = 2

    # Kolory do oznaczania statusu pojazdów.
    _colors = [(0, 255, 0), (0, 0, 255), (192, 192, 192)]

    def __init__(self, x, y, w, h, status=STATUS_NEW, timeTracked=0, timeUnknow=0, pixelDiff=0):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__status = status
        self.__timeTracked = timeTracked
        self.__timeUnknow = timeUnknow
        self.__pixelDiff = pixelDiff

    def __eq__(self, other):
        x, y, w, h = other.getCoordinates()
        return (self.__x, self.__y, self.__w, self.__h) == (x, y, w, h)

    def setStatus(self, newStatus):
        self.__status = newStatus

    def getStatus(self):
        return self.__status

    def getColor(self):
        return self._colors[self.__status]

    def getCoordinates(self):
        """ Zwraca lewy-górny punkt oraz szerokość i wysokość """
        return self.__x, self.__y, self.__w, self.__h

    def getTimeTracked(self):
        return self.__timeTracked

    def setTimeTracked(self, value):
        self.__timeTracked = value

    def getTimeUnknow(self):
        return self.__timeUnknow

    def setTimeUnknow(self, value):
        self.__timeUnknow = value

    def updateTimes(self):
        if self.__status == Vehicle.STATUS_TRACKED:
            self.__timeTracked = self.__timeTracked + 1

        if self.__status == Vehicle.STATUS_UNKNOW:
            self.__timeUnknow = self.__timeUnknow + 1

    def getPixelSpeed(self):
        return self.__pixelDiff

    def setPixelSpeed(self, value):
        self.__pixelDiff = value


def drawObjects(image, objects, linewidth=3):
    """Oznacza potencjalne pojazdy kolorami"""

    # sprawdź czy obrazj jest w formacie bgr i dokonaj ewentualnej konwersji
    img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) if len(image.shape) == 2 else image.copy()

    for obj in objects:
        x, y, w, h = obj.getCoordinates()
        point1 = (int(x), int(y))
        point2 = (int(x+w), int(y+h))
        cv2.rectangle(img, point1, point2, obj.getColor(), thickness=linewidth)

    return img