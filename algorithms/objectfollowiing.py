__author__ = 'rafal'

import cv2
from algorithms.objdetection import Obj, ObjectDetector

class ObjectFollower:

    currentlyFollowed = []

    def updateObjects(newObjects):

        # sprawdź który z aktualnie śledzonych obiektów odpowiada któremuś z nowych
        # jeżeli wśród starych obiektów jest jakiś który nie ma odpowiednika w nowych, to dodaj go do usunietych
        # dodaj pozostałe nowe obiekty do śledzonych
        pass

    def drawFollowedObjects(self, img):
        result = img.copy()
        for obj in self.currentlyFollowed:
            cv2.rectangle(result, obj.pt1, obj.pt2, ())






