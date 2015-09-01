__author__ = 'rafal'

from cv2 import destroyWindow, namedWindow, imshow


class Window:

    __id = 0

    def __init__(self, windowname=None, windowmode=cv2.WINDOW_FREERATIO):
        Window.__id += 1
        self.__name = "Window" + str(Window.__id)
        self.__mode = windowmode
        self.__windowCrated = False

    def __del__(self):
        destroyWindow(self.__name)

    def show(self, img):
        if not self.__windowCrated:
            namedWindow(self.__name, self.__mode)
            self.__windowCrated = True
        imshow(self.__name, img)
