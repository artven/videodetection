__author__ = 'rafal'
import cv2
import numpy as np

from utilities import keypressed
from managers.video import VideoReader
from managers.window import Window
from algorithms.bgsub import BackgroundSubtractor
from algorithms.objdetection import ObjectDetector
from algorithms.objectfollowing import ObjectFollower

if __name__ == "__main__":

    path = "videos/samples/samochód czerwony błonia.avi"
    inputVideo = VideoReader(path)
    outputWindow = Window()
    width, height = inputVideo.size()

    bgSub = BackgroundSubtractor()

    resultFrame = np.zeros([2*height, 2*width, 3], dtype=np.uint8)

    while not keypressed():
        frame = inputVideo.read()

        if inputVideo.isGood():

            substractedFrame = bgSub.apply(frame, mediansize=5)

            resultFrame[:height, :width, :] = frame
            resultFrame[:height, width:, :] = cv2.cvtColor(substractedFrame, cv2.COLOR_GRAY2BGR)
            resultFrame[height:, :width, :] = ObjectDetector.drawObjectsBorders(substractedFrame)

            objects = ObjectDetector.find(substractedFrame)
            ObjectFollower.updateObjects(objects)
            followed = ObjectFollower.drawFollowedObjects(frame)
            resultFrame[height:, width:, :] = followed

            outputWindow.show(resultFrame)
        else:
            break
