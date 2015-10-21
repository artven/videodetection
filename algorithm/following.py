__author__ = 'rafal'

import cv2
import numpy as np

from algorithm.objects import Vehicle
from utilities.frame import Frame

# from algorithm.contourdet import ContourDetector


class Follower:

    tracked = []
    border = 100
    distanceFromBorder = 50
    frameWidth = 0
    direction = "left2right"  # "right2left"

    detectedCarOnRight = False
    detectedCarOnLeft = False
    leftLock = False
    rightLock = False


    @staticmethod
    def update(newVehicles, frame, mask):

        height, width = frame.getSize()
        Follower.frameWidth = width

        result = []

        if Follower.direction == "right2left":
            for newCar in newVehicles:
                # detekcja z prawej strony
                if Follower.isCloseToRightBorder(newCar):
                    Follower.detectedCarOnRight = True
                    if not Follower.rightLock:
                        Follower.tracked.append((newCar, frame))
                        Follower.rightLock = True
                        print("nowy obiekt z prawej")
                # detekcja z lewej strony
                elif Follower.isCloseToLeftBorder(newCar):
                    Follower.detectedCarOnLeft = True
                    if not Follower.leftLock:
                        Follower.leftLock = True
                        print("nowy obiekt z lewej")
                        # pobierz ze stosu pojazd
                        if len(Follower.tracked):
                            oldCar, oldframe = Follower.tracked.pop()
                            result.append(newCar, frame, oldCar, oldframe, mask)
                        else:
                            print("Nie udało się pobrać danych o obiekcie!")
        elif Follower.direction == "left2right":
            for newCar in newVehicles:
                # detekcja z lewej strony
                if Follower.isCloseToLeftBorder(newCar):
                    Follower.detectedCarOnLeft = True
                    if not Follower.leftLock:
                        Follower.tracked.append((newCar, frame))
                        Follower.leftLock = True
                        print("nowy obiekt z lewej")
                elif Follower.isCloseToRightBorder(newCar):
                    Follower.detectedCarOnRight = True
                    if not Follower.rightLock:
                        Follower.rightLock = True
                        print("nowy obiekt z prawej")
                        # pobierz ze stosu pojazd
                        if len(Follower.tracked):
                            oldCar, oldframe = Follower.tracked.pop()
                        else:
                            print("Nie udało się pobrać danych o obiekcie!")

        if Follower.detectedCarOnRight == False:
            Follower.rightLock = False

        if Follower.detectedCarOnLeft == False:
            Follower.leftLocktLock = False






    @staticmethod
    def isCloseToLeftBorder(newCar):
        return newCar.centerx < (Follower.border + Follower.distanceFromBorder)

    @staticmethod
    def isCloseToRightBorder(newCar):
        return newCar.centerx > (Follower.frameWidth - Follower.border - Follower.distanceFromBorder)





