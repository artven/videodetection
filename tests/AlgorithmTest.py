__author__ = 'rafal'

import cv2
import numpy as np
import time

# narzędzia pomocnicze
from utilities.keys import keypressed
from utilities.video import VideoReader
from utilities.window import Window

# algorytm
from algorithm.core import algorithm

# przypadki testowe
f1 = "videos/samples/autobus akropol.avi"
f2 = "videos/samples/samochód biały akropol.avi"
f3 = "videos/samples/samochód bordowy akropol.avi"
f4 = "videos/samples/samochód czarny w tle akropol.avi"
f5 = "videos/samples/samochód srebrny akropol.avi"
f6 = "videos/samples/samochód zielony.avi"
f7 = "videos/samples/taksówka akropol.avi"


files = [f1, f2, f3, f4, f5, f6, f7]


for filename in files:
    nameParts = filename.split(sep='/')
    print(nameParts[-1])

    inputVideo = VideoReader("../" + filename)
    outputWindow = Window()
    width, height = inputVideo.size()

    while not keypressed():
        frame = inputVideo.read()

        if not inputVideo.isGood():
            break

        result = algorithm(frame, width, height)
        outputWindow.show(result)
