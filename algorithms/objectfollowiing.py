__author__ = 'rafal'

import cv2
from algorithms.objdetection import Obj, ObjectDetector

class ObjectFollower:

    currentlyFollowed = []

    @staticmethod
    def updateObjects(newObjects):

        # sprawdź który z aktualnie śledzonych obiektów odpowiada któremuś z nowych
        matchedObjects = []
        for obj in ObjectFollower.currentlyFollowed:
            for newObj in newObjects:
                if ObjectFollower.__areConnected(obj, newObj):
                    obj.update(newObj)
                    newObjects.remove(newObj)
                    matchedObjects.append(obj)
                    ObjectFollower.currentlyFollowed.remove(obj)


        # jeżeli wśród starych obiektów jest jakiś który nie ma odpowiednika w nowych, to dodaj go do usunietych

        ObjectFollower.currentlyFollowed = matchedObjects

        # dodaj pozostałe nowe obiekty do śledzonych
        for obj in newObjects:
            ObjectFollower.currentlyFollowed.append(obj)

        pass

    @staticmethod
    def drawFollowedObjects(img):
        result = img.copy()
        for obj in ObjectFollower.currentlyFollowed:
            cv2.rectangle(result, obj.pt1, obj.pt2, (255, 0, 0), thickness=3)
        return result



    @staticmethod
    def __areConnected(obj1, obj2):

        pass



