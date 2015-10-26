#!/usr/bin/env python3
__author__ = 'rafal'

import os


def clearConsole():
    os.system('clear')


# narzędzia pomocnicze
from utilities.keys import keypressed
from src.video import VideoReader
from utilities.window import Window
from utilities.frame import Frame

# algorytm
from src.core import algorithm
from src.analysis import getVehiclesData

# przypadki testowe
f1 = "videos/samples/autobus akropol.avi"
f2 = "videos/samples/samochód biały akropol.avi"
f3 = "videos/samples/samochód bordowy akropol.avi"
f4 = "videos/samples/samochód czarny w tle akropol.avi"
f5 = "videos/samples/samochód srebrny akropol.avi"
f6 = "videos/samples/samochód zielony.avi"
f7 = "videos/samples/taksówka akropol.avi"
f8 = "videos/full/2015-06-05-132225.webm"
f9 = "videos/full/2015-06-05-132408.webm"

# files = [f1, f2, f3, f4, f5, f6, f7, f8]

files = [f1, f2, f9]

for filename in files:

    # clearConsole()

    nameParts = filename.split(sep='/')
    print(nameParts[-1])

    inputVideo = VideoReader("../" + filename)
    outputWindow = Window()
    width, height = inputVideo.size()
    fps = inputVideo.fps()

    prevFrame = None

    while not keypressed():

        frame = Frame(inputVideo.read(), isFromCamera=True, fps=fps)

        if not inputVideo.is_good():
            break

        followedvehicles, allComponents, orgImg, subImg, objImg, followImg = algorithm(frame.img, width, height)
        outputWindow.show(allComponents)

        # wyliczanie parametrów
        if prevFrame is not None:
            getVehiclesData()

        # zapamiętanie poprzedniej ramki w celu policzenia prędkości
        prevFrame = Frame