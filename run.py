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
        vehicles, frame = preSelectVehicles(vehicles, frame)
        vehiclesRecords = Follower.update(vehicles, frame, mask)

        dataRecords = VehiclesClassifier.performRating(detectedVehiclesRecords)


        outputWindow.show(drawObjects(frame.img, vehicles))
