__author__ = 'rafal'
import cv2
import numpy as np
from managers.capture import CaptureManager
from algorithms.bgsub import BackgroundSubtractor

if __name__ == "__main__":

    source = "videos/samples/samochód czerwony błonia.avi"
    inputVideo = CaptureManager(source)
    bgSub = BackgroundSubtractor()

    width, height = inputVideo.size


    while 1:
        frame = inputVideo.read()

        if not inputVideo.is_good:
            break

        resultFrame = np.zeros([2*height, 2*width, 3], np.uint8)
        greyFrame = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        bgFrame = bgSub.apply(frame)

        resultFrame[:height, :width, :] = frame
        resultFrame[:height, width:, :] = greyFrame
        resultFrame[height:, :width, :] = cv2.cvtColor(bgFrame, cv2.COLOR_GRAY2BGR)

        inputVideo.show(resultFrame)

        key = cv2.waitKey(1) & 0xFF
        bgSub.control(key)
        if not inputVideo.control(key):
            break