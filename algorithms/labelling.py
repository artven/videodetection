__author__ = 'rafal'

import cv2
import numpy as np


def mark(frame, percent=0.005):
    height, width = frame.shape
    size = height * width
    result = np.zeros([height, width, 3])
    ret, marked_image = cv2.connectedComponents(frame)
    unique_markers = np.unique(marked_image)

    for marker in unique_markers:
        if marker != 0:
            # jeżeli obszar jest zbyt mały to go nie oznaczaj
            if np.count_nonzero(marked_image == marker)/size < percent:
                print(np.count_nonzero(marked_image == marker))
                result[marked_image == marker] = 0
            else:
                result[marked_image == marker] = __random_color()

    return result



def __random_color():
    from random import randint
    b = randint(0, 255)
    g = randint(0, 255)
    r = randint(0, 255)
    return b, g, r


