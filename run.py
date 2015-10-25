#!/usr/bin/env python3
__author__ = 'rafal'

import cv2
import numpy as np
import time
import os


def clearConsole():
    os.system('clear')


# narzędzia pomocnicze
from utilities.keys import keypressed
from utilities.video import VideoReader
from utilities.window import Window
from utilities.frame import Frame

# algorytm
from algorithm.core import algorithm
# from algorithm.analysis import getVehiclesData, printVehiclesData, preSelectVehicles
from algorithm.analysis import preSelectVehicles
from algorithm.objects import drawObjects
from algorithm.following import Follower
from algorithm.classification import VehiclesClassifier
from algorithm.colordet import ColorDetector
from algorithm.contourdet import ContourDetector
from algorithm.sizedet import SizeMeasurment
from algorithm.speeddet import SpeedMeasurment

# przypadki testowe
f1 = 'videos/samples/autobus akropol.avi'
f2 = 'videos/samples/samochód biały akropol.avi'
f3 = 'videos/samples/samochód bordowy akropol.avi' # left2right
f4 = 'videos/samples/samochód czarny w tle akropol.avi'
f5 = 'videos/samples/samochód srebrny akropol.avi'
f6 = 'videos/samples/samochód zielony.avi'  # left2right
f7 = 'videos/samples/taksówka akropol.avi'
f8 = 'videos/full/2015-06-05-132225.webm'
f9 = 'videos/full/2015-06-05-132408.webm'

# files = [f1, f2, f3, f4, f5, f6, f7, f8]

# files = [f1, f2, f9]

foundCars = []

files = [f3]

for filename in files:

    inputVideo = VideoReader(filename)
    outputWindow = Window()
    width, height = inputVideo.size()
    fps = inputVideo.getFPS()

    frameId = 0
    while not keypressed():

        frame = Frame(inputVideo.read(), isFromCamera=True, fps=fps, frameNr=frameId)
        frameId = frameId + 1

        if not inputVideo.isGood():
            break

        vehicles, mask = algorithm(frame)
        vehicles, frame = preSelectVehicles(vehicles, frame, drawLines=False)
        vehiclesRecords = Follower.update(vehicles, frame, mask)

        if vehiclesRecords is not None:
            foundCars.extend(vehiclesRecords)

        dataRecords = VehiclesClassifier.performRating(vehiclesRecords)

        # if dataRecords is not None:
        #    print(dataRecords)

        outputWindow.show(drawObjects(frame.img, vehicles))

    print("znaleziono samochodów: " + str(len(foundCars)))

    if len(foundCars):
        car = foundCars[0]

        newCar, frame, oldCar, oldframe, mask = car
        x, y, w, h = newCar.getCoordinates()
        image = frame.img[y:y+h, x:x+w, :]
        # mask = mask[y:y+h, x:x+w]

        colorBar, color = ColorDetector.findColor(image)
        cv2.namedWindow("kolor", cv2.WINDOW_FREERATIO)
        # cv2.imshow("kolor", colorBar)
        print(color)

        cv2.namedWindow("maska", cv2.WINDOW_FREERATIO)
        cv2.imshow("maska", mask)

        cwidth = SizeMeasurment.calculateWidth(newCar)
        print("Długość pojazdu wynosi " + str(cwidth))

        cheight = SizeMeasurment.calculateHeight(newCar)
        print("Wysokość pojazdu wynosi " + str(cheight))

        carea = SizeMeasurment.calculateArea(newCar, mask)
        print("Pole pojazdu wynosi " + str(carea))

        speed = SpeedMeasurment.calculateSpeed(newCar, frame, oldCar, oldframe)
        print("Prędkośc pojazdu")

        frame.img = SizeMeasurment.drawSizeInfo(frame.img, newCar, mask, cwidth, cheight, carea)
        frame.img = ColorDetector.drawColorBar(frame.img, colorBar)

        cv2.namedWindow("all")
        cv2.imshow("all", frame.img)

        outputWindow.show(image)

    while not keypressed():
        pass

    cv2.destroyAllWindows()