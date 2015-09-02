__author__ = 'rafal'

import cv2
import numpy as np


class VideoReader:

    # Read data from device or file.

    def __init__(self, videosource=0):
        self.__cap = cv2.VideoCapture(videosource)
        self.__good = self.__cap.isOpened()
        self.__frame = None
        self.__run = True

    def __del__(self):
        self.__cap.release()

    def read(self):
        if not self.__run:
            return self.__frame

        if not self.__good:
            raise RuntimeError("Source is broken!")

        ret, newframe = self.__cap.read()
        if not ret:
            self.__good, self.__frame = False, None
        else:
            self.__good, self.__frame = True, newframe

        return self.__frame

    # video properties

    def isGood(self):
        return self.__good

    def getPositionMseconds(self):
        return self.__cap.get(cv2.CAP_PROP_POS_MSEC)

    def setPositionMseconds(self, value):
        self.__cap.set(cv2.CAP_PROP_POS_MSEC, value)

    def getPositionFrames(self):
        return self.__cap.get(cv2.CAP_PROP_POS_FRAMES)

    def setPositionFrames(self, value):
        self.__cap.set(cv2.CAP_PROP_POS_FRAMES, value)

    def getFPS(self):
        return self.__cap.get(cv2.CAP_PROP_FPS)

    def getFramesCount(self):
        return self.__cap.get(cv2.CAP_PROP_FRAME_COUNT)

    def size(self):
        return int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # video control

    def stopReading(self):
        self.__run = False

    def startReading(self):
        self.__run = True

    def framesForward(self, step=1):
        if step <= 0:
            raise AttributeError("Wrong number of frames to move forward!")

        currentPosition = self.getPositionFrames()
        maxPostion = self.getFramesCount()
        newPostion = min(currentPosition+step, maxPostion)
        self.setPositionFrames(newPostion)

    def framesBackward(self, step=-1):
        if step >= 0:
            raise AttributeError("Wrong number of frames to move backward!")

        currentPosition = self.getPositionFrames()
        maxPostion = self.getFramesCount()
        newPostion = max(currentPosition-step, 0)
        self.setPositionFrames(newPostion)