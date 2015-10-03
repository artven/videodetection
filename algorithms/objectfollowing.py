__author__ = 'rafal'

import cv2
import numpy as np
from algorithms.objdetection import Obj, ObjectDetector
from algorithms.contourdet import ContourDetector


class ObjectFollower:

    currentlyFollowed = []

    @staticmethod
    def updateObjects(newObjects):

        # sprawdź który z aktualnie śledzonych obiektów odpowiada któremuś z nowych
        matchedObjects = []
        for obj in ObjectFollower.currentlyFollowed:
            for newObj in newObjects:
                if ObjectFollower.areConnected(obj, newObj):
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
            cv2.rectangle(result, obj.getPt1(), obj.getPt1(), (255, 0, 0), thickness=3)
        return result

    @staticmethod
    def areConnected(obj1, obj2):
        # Checks if objects have common part
        x1, y1, w1, h1 = obj1.getRectangle()
        x2, y2, w2, h2 = obj2.getRectangle()

        return ((x2 <= x1 + w1) if (x1 < x2) else (x1 <= x2 + w2)) and \
               ((y2 <= y1 + h1) if (y1 < y2) else (y1 <= y2 + h2))

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



