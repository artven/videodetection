__author__ = 'rafal'

import cv2


class BackgroundSubtractor:


    def __init__(self, subtype=0):

        self.__fgbg = cv2.createBackgroundSubtractorMOG2()
        self.__run = True
        self.__lastFrame = None

    def apply(self, frame, op=cv2.MORPH_OPEN, kernel=cv2.MORPH_ELLIPSE, kernelsize=(3, 3),
              mediansize=3, dilateiter=1):
        # apply(self, frame, [op, kernel, kernelsize, mediansize, dilateiter]) -> substractedFrame
        # Substract obcjects from image.
        if self.__run:
            substractedFrame = self.__fgbg.apply(frame)
            filteredFrame = self.__filterImage(substractedFrame, op, kernel, kernelsize, mediansize, dilateiter)
            self.__lastFrame = filteredFrame
        return self.__lastFrame

    def stop(self):
        self.__run = True

    def start(self):
        self.__run = False

    @staticmethod
    def __filterImage(img, op, kernel, kernelsize, mediansize, dilateiter):
        # Additional filtering for result improvement
        ker = cv2.getStructuringElement(kernel, kernelsize)
        morphframe = cv2.morphologyEx(img, op, ker)
        medianframe = cv2.medianBlur(morphframe, mediansize)
        dilatframe = cv2.dilate(medianframe, ker, iterations=dilateiter)
        return dilatframe