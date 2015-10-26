__author__ = 'rafal'

import cv2


class Vehicle:

    STATUS_NEW = 0
    STATUS_TRACKED = 1
    STATUS_UNKNOW = 2

    # Kolory do oznaczania statusu pojazdów.
    _colors = [(0, 255, 0), (0, 0, 255), (192, 192, 192)]

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.centerx = x+int(w/2)
        self.centery = y+int(h/2)

    def __eq__(self, other):
        x, y, w, h = other.getCoordinates()
        return (self.__x, self.__y, self.__w, self.__h) == (x, y, w, h)

    def getCoordinates(self):
        """ Zwraca lewy-górny punkt oraz szerokość i wysokość """
        return int(self.x), int(self.y), int(self.w), int(self.h)


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


def drawObjects(image, objects, linewidth=2):
    """Oznacza potencjalne pojazdy kolorami"""

    # sprawdź czy obrazj jest w formacie bgr i dokonaj ewentualnej konwersji
    img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) if len(image.shape) == 2 else image.copy()

    for obj in objects:
        # oznacz granice obiektu
        x, y, w, h = obj.getCoordinates()
        point1 = (x, y)
        point2 = (x+w, y+h)
        cv2.rectangle(img, point1, point2, obj.getColor(), thickness=linewidth+2)

        # oznacz centrum obiektu
        cenx = obj.centerx
        ceny = obj.centery

        point1 = (cenx, ceny-10)
        point2 = (cenx, ceny+10)
        cv2.line(img, point1, point2, obj.getColor(), thickness=linewidth)


        point1 = (cenx-10, ceny)
        point2 = (cenx+10, ceny)
        cv2.line(img, point1, point2, obj.getColor(), thickness=linewidth)


    return img

class Frame:
    # Klasa opakowywujacą klatkę obrazu.

    def __init__(self, inputVideo):

        # Sprawdź czy plik źródłowy jest podany w postaci napisu.
        # Jeśli tak, oznacza to, że został odczytany plik.
        # W przeciwynym przypadku obraz pochodzi bezpośrednio z kamery.
        if isinstance(inputVideo.source, str):
            self.isFromCamera = False
        else:
            self.isFromCamera = True

        self.img = inputVideo.read()
        self.creationTime = datetime.now()
        self.fps = inputVideo.getFPS()
        self.framePos = inputVideo.getPositionFrames()

    def isBGR(self):
        return len(self.img.shape) == 3

    def isFromCamera(self):
        return self.isFromCamera

    def getSize(self):
        """Zwraca wysokość i szerokość obrazu."""
        return self.img.shape[0], self.img.shape[1]