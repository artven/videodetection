__author__ = 'rafal'

from cv2 import destroyWindow, namedWindow, imshow
import cv2

class Window:

    __id = 0

    def __init__(self, windowmode=cv2.WINDOW_FREERATIO):
        Window.__id += 1
        self.__name = "Window" + str(Window.__id)
        self.__mode = windowmode
        namedWindow(self.__name, self.__mode)

    def __del__(self):
        destroyWindow(self.__name)

    def show(self, img):
        imshow(self.__name, img)
