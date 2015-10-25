__author__ = 'rafal'

from algorithm.core import convertBGR2Gray
from algorithm.objects import Vehicle


from utilities.frame import Frame

import cv2
import numpy as np

def preSelectVehicles(vehicles, frame, border=200, horizontalborder=50, drawLines=True):
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

