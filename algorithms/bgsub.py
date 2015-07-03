__author__ = 'rafal'

import cv2


class BackgroundSubtractor:
    MOG2, KNN = 0, 1

    def __init__(self, subtype=0):
        """
        :param subtype: Typ silnika wyodrębniania tła - BackgroundSubtractor.MOG2/KNN
        """

        self.__fgbg = cv2.createBackgroundSubtractorMOG2() if subtype == 0 else cv2.createBackgroundSubtractorKNN()
        self.__run = True
        self.__lastFrame = None

    def apply(self, frame, op=cv2.MORPH_OPEN, kernel=cv2.MORPH_ELLIPSE, kernelsize=(3, 3),
              mediansize=3, dilateiter=1):
        """Uzyskiwanie tła na podstawie klatki.
        Funckja przetwarza kolejne klatki, wyodrębnia tło na podstawie sumy ważonej poprzednich klatek.
        Wynik wyodrębniania tła jest poddawany obróbce(morfologiczna->mediana->dylatacja),
        w celu wyraźnej separacji wyodrębnionych obiektów pierwszoplanowych.
        :param frame: Ramka obrazu wejściowego.
        :param op: Typ operacji morfologicznej - cv2.MORPH_*.
        :param kernel: Jądro przekształcenia morfologicznego.
        :param kernel: Jądro przekształcenia morfologicznego.
        :param mediansize: Rozmiar filtru medianowego.
        :param dilateiter: Liczba wykonywanych dylatacji obrazu.
        :return: Binarna ramka obrazu z wyodrębnionym tłem.
        """

        ker = cv2.getStructuringElement(kernel, kernelsize)
        if not self.__run:
            return self.__lastFrame

        newframe = self.__fgbg.apply(frame)
        morphframe = cv2.morphologyEx(newframe, op, ker)
        medianframe = cv2.medianBlur(morphframe, mediansize)
        dilatframe = cv2.dilate(medianframe, ker, iterations=dilateiter)
        self.__lastFrame = dilatframe

        return self.__lastFrame

    def control(self, key=None):
        """Sterowanie procesem wyodrębniania.
        Funkcja pozwala włączać/wyłączać proces substrakcji poprzez przekzanie klawisza.
        Klawisz 's' spowoduje zatrzymanie operacji.
        :param key: Klawisz(znak) sterujący.
        """

        if key is None:
            key = cv2.waitKey(1) & 0xFF

        self.__run = not self.__run if key == ord('s') else self.__run
