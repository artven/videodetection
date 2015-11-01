__author__ = 'rafal'

import cv2
import numpy as np
from datetime import datetime

# TODO dopisać poprawne komentarze


class VideoReader:

    def __init__(self, videosource=0):
        self.source = videosource
        self.__cap = cv2.VideoCapture(videosource)
        self.__good = self.__cap.isOpened()
        self.__frame = None

    def __del__(self):
        self.__cap.release()

    def read(self):
        ret, image = self.__cap.read()
        if not ret:
            self.__good = False
            return None

        return image

    def is_good(self):
        return self.__good

    def position_mseconds(self):
        return self.__cap.get(cv2.CAP_PROP_POS_MSEC)

    def position_frames(self):
        return self.__cap.get(cv2.CAP_PROP_POS_FRAMES)

    def fps(self):
        return self.__cap.get(cv2.CAP_PROP_FPS)

    def frames_count(self):
        return self.__cap.get(cv2.CAP_PROP_FRAME_COUNT)

    def size(self):
        return int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


class VideoWriter:

    forucc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    format = ".avi"
    fps = 20
    folder = "videos/"

    def __init__(self, size=(640, 480)):
        self.__filename = VideoWriter.folder + str(datetime.now())[0:-7] + VideoWriter.format
        self.__size = size
        self.__writer = cv2.VideoWriter(self.__filename, VideoWriter.forucc, VideoWriter.fps, self.__size)

    def __del__(self):
        self.__writer.release()

    def write(self, frame):
        if self.__writer.isOpened():
            self.__writer.write(frame)


class Window:

    __id = 0

    def __init__(self, windowmode=cv2.WINDOW_FREERATIO):
        Window.__id += 1
        self.__name = "Window" + str(Window.__id)
        self.__mode = windowmode
        cv2.namedWindow(self.__name, self.__mode)

    def __del__(self):
        cv2.destroyWindow(self.__name)

    def show(self, img):
        cv2.imshow(self.__name, img)

    def get_name(self):
        return self.__name


class Frame:
    # Klasa opakowywujacą klatkę obrazu.

    def __init__(self, inputVideo):

        # Sprawdź czy plik źródłowy jest podany w postaci napisu.
        # Jeśli tak, oznacza to, że został odczytany plik.
        # W przeciwynym przypadku obraz pochodzi bezpośrednio z kamery.
        if isinstance(inputVideo.source, str):
            self.isFromCamera = False
        else:
            self.isFromCamera = True

        self.img = inputVideo.read()
        self.creationTime = datetime.now()
        self.fps = inputVideo.fps()
        self.framePos = inputVideo.position_frames()

    def size(self):
        """Zwraca wysokość i szerokość obrazu."""
        return self.img.shape[0], self.img.shape[1]