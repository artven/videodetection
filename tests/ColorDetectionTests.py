# import the necessary packages

import cv2
import numpy as np
from sklearn.cluster import KMeans
from utilities.keys import keypressed

def centroidHistogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


def plotColors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
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


def findDominantColorsBar(image, colorsN=4):
    # http://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster the pixel intensities
    clt = KMeans(n_clusters = colorsN)
    clt.fit(image)

    # build a histogram of clusters and then create a figure
    # representing the number of pixels labeled to each color
    hist = centroidHistogram(clt)

    resultColors = []
    resultPercents = []

    percents = hist
    colors = clt.cluster_centers_ # BGR

    for col in colors:
        resultColors.append( ((int(col[0])), int(col[1]), int(col[2])))

    for pen in percents:
        resultPercents.append(round(pen, 3))

    return bar, resultColors, resultPercents

def findColor(img):
    _, colors, percents = findDominantColorsBar(image, colorsN=4)
    bestPercent = max(percents)
    bestPercentIndex = percents.index(bestPercent)
    color = colors[bestPercentIndex]
    colorBar = np.zeros([100, 100, 3], dtype=np.uint8)
    colorBar[:, : , :] = color
    return colorBar, color


image = cv2.imread("pokemony.png")
x, y, w, h = 200, 20, 250, 250
image = image[x:x+w, y:y+h, :]

inputWindow = "input image"
cv2.namedWindow(inputWindow, cv2.WINDOW_FREERATIO)
cv2.imshow(inputWindow, image)

outputWindow = "bar"
cv2.namedWindow(outputWindow, cv2.WINDOW_FREERATIO)
bar, color= findColor(image)
cv2.imshow(outputWindow, bar)

print("Best color=", str(color))


while not keypressed():
    pass

cv2.destroyAllWindows()


