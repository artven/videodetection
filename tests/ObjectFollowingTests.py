__author__ = 'rafal'

import numpy as np

from utilities import keypressed
from src.video import VideoReader
from utilities.window import Window


if __name__ == "__main__":

    file = "videos/samples/autobus akropol.avi"
    inputVideo = VideoReader(file)

    resultWindow = Window()
    width, height = inputVideo.size()
    resultFrame = np.zeros([2*height, 2*width, 3], dtype=np.uint8)

    while not keypressed():
        if inputVideo.is_good():
            frame = inputVideo.read()
            resultFrame[:height, :width, :] = frame
            resultWindow.show(resultFrame)
        else:
            break


