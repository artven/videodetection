__author__ = 'rafal'

from algorithm.core import convertBGR2Gray
from algorithm.objects import Vehicle


from utilities.frame import Frame

import cv2
import numpy as np

def preSelectVehicles(vehicles, frame, border=100, horizontalborder=50, drawLines=True):
    """Dokonaj selekcji obiektów, które nie znajdują się przy krawędzi."""
    height, width = frame.getSize()
    result = []

    for vehic in vehicles:
        if (vehic.centerx > border) and (vehic.centerx < width-border) and (vehic.centery>horizontalborder) and \
                (vehic.centery < height-horizontalborder):
            result.append(vehic)

    if drawLines:
        leftUpperPoint = (border, horizontalborder)
        rightUpperPoint = (width-border, horizontalborder)
        leftLowerPoint = (border, height-horizontalborder)
        rightLowerPoint = (width-border, height-horizontalborder)
        frame.img = cv2.line(frame.img, leftLowerPoint, leftUpperPoint, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, leftLowerPoint, rightLowerPoint, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, rightLowerPoint, rightUpperPoint, (0, 0, 255), thickness=3)
        frame.img = cv2.line(frame.img, leftUpperPoint, rightUpperPoint, (0, 0, 255), thickness=3)

    return result, frame


class Classi

class SpeedCalculator():

    pixelRange = 200
    metersRange = 10

    @staticmethod
    def calculate(car, frame, oldcar, oldframe):

        newX = car.centerx


        pass





"""
def getVehiclesData(vehicles, frame, prevFrame, prevVehicles, mask=None):
    result = []

    if (prevFrame is None) or (prevVehicles is None):
        return result

    def findClosestVehicle(orginalVehicle, Vehicles, distanceLimit=50):
        if len(Vehicles) == 0:
            return None

        distances = []

        for veh in Vehicles:
            dist = orginalVehicle.centerx - veh.centerx
            distances.append(dist)

        minimalDistance = min(distances)

        if minimalDistance > distanceLimit:
            return None

        minimumDistanceIndex = distances.index(minimalDistance)
        return Vehicles[minimumDistanceIndex]

    for veh in vehicles:

        res = findClosestVehicle(veh, prevVehicles)

        if res is None:

            continue
        else:
            if res in prevVehicles:
                prevVehicles.remove(res)

            if res.centerx == veh.centerx:
                continue

            record = {}
            record['x, y, h, w'] = (veh.x, veh.y, veh.w, veh.h)
            record['center'] = (veh.centerx, veh.centery)
            record['diff'] = veh.centerx - res.centerx

            result.append(record)


    if len(result) == 0:
        return None
    else:
        return result


def printVehiclesData(dataRecords):

    if len(dataRecords):
        print("Vehicles number = %d", len(dataRecords))

    for record in dataRecords:
        print(record)

"""
'''
    # if prevFrame is None:
    #   raise AttributeError("algorithm.analysis.getVehiclesInfo: poprzednia ramka nie może być pusta!")

    # Wyliczenie maski obiektu.
    mask = convertBGR2Gray(substractedImg)

    result = []
    for veh in vehicles:
        x, y, w, h = veh.getCoordinates()
        # color = ColorDetection.findDominantColor(veh, frame.img, mask)
        # size = SizeMeasurement.calculate(veh, mask)
        # speed = SpeedMeasurement.calculate(veh, frame, prevFrame)

        # record = {"x": round(x), "y": round(y), "w": round(w), "h": round(h), "color": color,
        #          "size": size, "speed": speed}
        result.append((x, y, w, h))

    return result
'''

class ColorDetection():


    hueUpperBound = 10
    hueLowerBound = 10
    saturationUpperBound = 10
    saturationLowerBound = 10
    valueUpperBound = 10
    valueLowerBound = 10

    __colors = {
        0: ((0, 0, 0), "Black"),
        1: ((255, 255, 255), "White"),
        2: ((0, 0, 255), "Red"),
        3: ((0, 255, 0), "Lime"),
        4: ((255, 0, 0), "Blue"),
        5: ((0, 255, 255), "Yellow"),
        6: ((255, 255, 0), "Cyan"),
        7: ((255, 0, 255), "Magenta"),
        8: ((192, 192, 192), "Silver"),
        9: ((128, 128, 128), "Gray"),
        10: ((0, 128, 0), "Green"),
        11: ((128, 0, 0), "Navy")
    }

    @staticmethod
    def findDominantColor(vehicle, img, mask):

        x, y, w, h = vehicle.getCoordinates()

        imgBGR = img[y:(y+h), x:(x+w), :]
        imgHSV = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2HSV)
        mask = mask[x:x+w, y:y+h]
        pixelCount = float(np.count_nonzero(mask))

        colorDetectionResults = []

        # Sprawdź wszystkie kolory
        for i in range(12):

            bgrUnitColor = np.uint8([[ColorDetection.__colors[i][0]]])
            hsvUnitColor = cv2.cvtColor(bgrUnitColor, cv2.COLOR_BGR2HSV)[0][0]

            hue, sat, val = hsvUnitColor[0], hsvUnitColor[1], hsvUnitColor[2]

            hueUpper = min(179, hue+ColorDetection.hueUpperBound)
            hueLower = max(0, hue-ColorDetection.hueLowerBound)
            satUpper = min(255, sat+ColorDetection.saturationUpperBound)
            satLower = max(0, sat-ColorDetection.saturationLowerBound)
            valUpper = min(255, val+ColorDetection.valueUpperBound)
            valLower = max(0, val-ColorDetection.valueLowerBound)

            lower = np.array([hueLower, satLower, valLower])
            upper = np.array([hueUpper, satUpper, valUpper])

            colorMask = cv2.inRange(imgHSV, lower, upper)
            res = cv2.bitwise_and(colorMask, colorMask, mask=mask)
            resCount = float(np.count_nonzero(res))
            colorDetectionResults.append(resCount/pixelCount)

        bestColor = max(colorDetectionResults)
        bestColorIndex = colorDetectionResults.index(bestColor)

        return (ColorDetection.__colors[bestColorIndex])[1]
