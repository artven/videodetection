__author__ = 'rafal'

from datetime import datetime


class Frame:
    # Klasa opakowywujacą klatkę obrazu.

    def __init__(self, img=None, time=None, isFromCamera=False, fps=None, frameNr=0):
        self.img = img
        self.__creationTime = datetime.now()
        self.__fromCamera = isFromCamera
        self.__fps = fps
        self.frameNr = frameNr

    def isBGR(self):
        return len(self.img.shape) == 3

    def isFromCamera(self):
        return self.__fromCamera

    def getSize(self):
        """Zwraca wysokość i szerokość obrazu."""
        return self.img.shape[0], self.img.shape[1]

    def getFPS(self):
        return self.__fps

    def getTime(self):
        return self.__creationTime