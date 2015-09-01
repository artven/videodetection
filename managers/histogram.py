__author__ = 'rafal'

import cv2
import numpy as np
from matplotlib import pyplot as plt

class HistogramManager:

    def __init__(self):
        self.__hist = None
        self.__image = None
        self.__channels = None

    def calculate(self, image, channels, mask=None, hist_size=256, range=[0, 256]):
        """Wylicz histogram obrazu.
        Funkcja wylicza histogram z obrazu dla wskazanego kanału.
        :param image: Obraz wejściowy.
        :param channels: Kanały obrazu. Dla obrazu rgb 0,1,2, dla obrazu szarego 0.
        :param mask: Opcjonalna maska umożliwiająca obliczenie histogramu dla wskazanego obszaru.
        :param hist_size: Rozmiar.
        :param range: Szerokość przedziału.
        :return: Obliczony histogram.
        """
        self.__image = image
        self.__channels = 3 if len(image.shape) == 3 else 1
        self.__hist = cv2.calcHist([image], [channels], mask, [hist_size], range)
        return self.__hist


    def plot(self):


        plt.plot

        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([img],[i],None,[256],[0,256])
            plt.plot(histr,color = col)
            plt.xlim([0,256])

        plt.show()



if __name__ == "__main__":

    print("HistogramManager!")












