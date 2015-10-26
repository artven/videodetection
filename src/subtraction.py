__author__ = 'rafal'

import cv2


class Subtractor:
    # Klasa wyodrębniająca tło oraz poruszające się elementy na obrazie.

    # Silnik wyodrębniania tła.
    __substractor = cv2.createBackgroundSubtractorMOG2()

    # Parametry filtracji obrazu.
    __op = cv2.MORPH_OPEN
    __kernel = cv2.MORPH_ELLIPSE
    __kernelsize = (3, 3)
    __mediansize = 5
    __dilateiter = 5

    @staticmethod
    def apply(frame):
        """
        Dokonuje wyodrębnienia tła z klatki obrazu. Zwraca zbinearyzowany obraz.
        """

        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        substractedFrame = Subtractor.__substractor.apply(frame)
        filteredFrame = Subtractor.__filter(substractedFrame)
        return filteredFrame

    @staticmethod
    def __filter(frame):
        """
        Dokonuje filtracji za pomocą mediany i dylatacji.
        """
        ker = cv2.getStructuringElement(Subtractor.__kernel, Subtractor.__kernelsize)
        morphframe = cv2.morphologyEx(frame, Subtractor.__op, ker)
        medianframe = cv2.medianBlur(morphframe, Subtractor.__mediansize)
        dilatframe = cv2.dilate(medianframe, ker, iterations=Subtractor.__dilateiter)
        return dilatframe
