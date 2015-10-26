__author__ = 'rafal'

import numpy as np
import cv2

# Przy implementacji modułu skorzystano z materiałów:
# http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# http://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

from sklearn.cluster import KMeans


class ColorDetector:
    # Klasa określająca kolor pojazdu.

    # Liczba kolorów wyszukiwanych w obrazie.
    __colorNumber = 5

    # Wysokość i szerokość zwracanego obrazu z konsoli.
    __barHeight = 50
    __barWidth = 300

    @staticmethod
    def __centroidHistogram(clt):
        """
        Przydziala wartości histogramu do zdefiniowanych grup. Dokonuje normalizacji nowego histogramu.
        :param clt: Zdefiniowane przez KMeans grupy.
        :return: Histogram po przydziale pikseli.
        """

        # Przydziel piksele względem grup.
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)

        # Znormalizuj histogram.
        hist = hist.astype("float")
        hist /= hist.sum()

        # Zwróć nowy histogram.
        return hist

    @staticmethod
    def __findDominantColors(image, n):
        """
        Znajduje n najbardziej dominujących kolorów na obrazie.
        :param image: badany obraz.
        :param n: liczba poszukiwanych kolorów.
        :return: lista znalezionych kolorów, procent powierzni kolorów.
        """
        
        # Przekształć obraz w listę pixeli.
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        # Podziel obraz na grupy.
        clt = KMeans(n_clusters=n)
        clt.fit(image)

        # Oblicz histogram nowego obrazu.
        hist = ColorDetector.__centroidHistogram(clt)

        # Dokonaj konwersji i zaokrąglenia wyników.
        percents = hist
        colors = clt.cluster_centers_  # BGR

        colorBar = ColorDetector.__createColorsBar(hist, clt.cluster_centers_)

        resultColors = []
        resultPercents = []

        for col in colors:
            resultColors.append( ((int(col[0])), int(col[1]), int(col[2])))
        for pen in percents:
            resultPercents.append(round(pen, 3))

        return resultColors, resultPercents, colorBar

    @staticmethod
    def __createColorsBar(hist, centroids):

        w = ColorDetector.__barWidth
        h = ColorDetector.__barHeight

        # initialize the bar chart representing the relative frequency
        # of each of the colors
        bar = np.zeros((h, w, 3), dtype=np.uint8)
        startX = 0

        # loop over the percentage of each cluster and the color of
        # each cluster
        for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
            startX = endX

        # return the bar chart
        return bar


    @staticmethod
    def findColor(image):
        """
        Przeprowadza analizę dominujących kolorów, wybiera z nich największy.
        :param image: przeszukiwany obraz.
        :return: obraz wypełniony kolorem, wartość koloru.
        """

        # Znajdź najlepsze kolory.
        colors, percents, colorBar = ColorDetector.__findDominantColors(image, n=ColorDetector.__colorNumber)

        # Wybierz największy kolor.
        bestPercent = max(percents)
        bestPercentIndex = percents.index(bestPercent)
        color = colors[bestPercentIndex]

        # Stwórz obraz reprezentujący znaleziony kolor.
        h = ColorDetector.__barHeight
        w = ColorDetector.__barWidth


        return colorBar, color

    @staticmethod
    def drawColorBar(img, colorBar):
        width = ColorDetector.__barWidth
        height = ColorDetector.__barHeight
        img[:height, :width, :] = colorBar
        return img