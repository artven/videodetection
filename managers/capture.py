__author__ = 'rafal'

import cv2
import numpy as np


class CaptureManager:
    """
    Klasa obsługująca odczyt obrazu video z pliku/kamery.
    """

    __id = 0

    __pos_msec = cv2.CAP_PROP_POS_MSEC            # Current position in milliseconds or video capture timestamp.
    __pos_frames = cv2.CAP_PROP_POS_FRAMES        # 0-based index of the frame to be decoded/captured next.
    __pos_ratio = cv2.CAP_PROP_POS_AVI_RATIO  # Relative position: 0 - start, 1 - end.
    __width = cv2.CAP_PROP_FRAME_WIDTH        # Width of the frames in the video stream.
    __height = cv2.CAP_PROP_FRAME_HEIGHT      # Height of the frames in the video stream.
    __fps = cv2.CAP_PROP_FPS                  # Frame rate.
    __forucc = cv2.CAP_PROP_FOURCC            # 4-character code of codec.
    __frame_count = cv2.CAP_PROP_FRAME_COUNT  # Number of frames in the video file.
    __format = cv2.CAP_PROP_FORMAT            # Format of the Mat objects returned by retrieve().
    __mode = cv2.CAP_PROP_MODE                # Backend-specific value indicating the current capture mode.

    # Only for cameras!
    __brightness = cv2.CAP_PROP_BRIGHTNESS   # Brightness of the image.
    __contrast = cv2.CAP_PROP_CONTRAST       # Contrast of the image.
    __saturation = cv2.CAP_PROP_SATURATION   # Saturation of the image.
    __hue = cv2.CAP_PROP_HUE                 # Hue of the image.
    __gain = cv2.CAP_PROP_GAIN               # Gain of the image.
    __exposure = cv2.CAP_PROP_EXPOSURE       # Exposure (only for cameras).
    __conver_rgb = cv2.CAP_PROP_CONVERT_RGB  # Flags indicating whether images should be converted to RGB.

    def __init__(self, source=0):
        CaptureManager.__id += 1
        self.__id = CaptureManager.__id
        self.__name = "Capture " + str(self.__id)
        self.__source = source
        self.__cap = cv2.VideoCapture(source)
        self.__good = self.__cap.isOpened()
        self.__frame = None
        self.__run = True
        self.__window = False

    def read(self):
        if self.__run:
            ret, frame = self.__cap.read()

            if not ret:
                self.__good = False
            else:
                self.__good = True
                self.__frame = frame

        return self.__frame

    @property
    def is_good(self):
        return self.__good

    @property
    def name(self):
        return self.__name

    def __del__(self):
        if self.__window:
            cv2.destroyWindow(self.name)

        self.__cap.release()

    def show(self, frame=None):
        if not self.__window:
            self.__window = True
            cv2.namedWindow(self.name, cv2.WINDOW_FREERATIO)

        cv2.imshow(self.name, frame if frame is not None else self.read())

    def control(self, key=None):
        k = cv2.waitKey(1) & 0xFF

        # wyjscie z programu
        if k == ord('q'):
            return False

        # zatrzymanie odczytu klatek
        if k == ord('s'):
            self.__run = not self.__run

        # klatka do przodu
        if k == ord('d'):
            new_pos = self.pos_frames+1 if self.pos_frames+1 != self.frame_count else self.frame_count
            self.pos_frames = new_pos
            _, self.__frame = self.__cap.read()
            self.pos_frames = new_pos

        # klatka do tyłu
        if k == ord('a'):
            new_pos = self.pos_frames-1 if self.pos_frames-1 != 0 else 0
            self.pos_frames = new_pos
            _, self.__frame = self.__cap.read()
            self.pos_frames = new_pos

        return True

    # właściwości obrazu video

    @property
    def msec(self):
        return self.__cap.get(CaptureManager.__pos_msec)

    @property
    def fps(self):
        return self.__cap.get(CaptureManager.__fps)

    @property
    def pos_frames(self):
        return self.__cap.get(CaptureManager.__pos_frames)

    @property
    def pos_ratio(self):
        return self.__cap.get(CaptureManager.__pos_ratio)

    @property
    def size(self):
        width = self.__cap.get(CaptureManager.__width)
        heigt = self.__cap.get(CaptureManager.__height)
        return width, heigt

    @property
    def forucc(self):
        return self.__cap.get(CaptureManager.__forucc)

    @property
    def frame_count(self):
        return self.__cap.get(CaptureManager.__frame_count)

    @property
    def format(self):
        return self.__cap.get(CaptureManager.__format)

    @property
    def mode(self):
        return self.__cap.get(CaptureManager.__mode)

    @msec.setter
    def msec(self, value):
        self.__cap.set(CaptureManager.__pos_msec, value)

    @pos_frames.setter
    def pos_frames(self, value):
        self.__cap.set(CaptureManager.__pos_frames, value)


if __name__ == "__main__":

    property("CaptureManager:")
    for field in dir(CaptureManager):
        if "_CaptureManager" and "__" not in field:
            print(field)

    source = "../videos/full/2015-06-05-134119.webm"
    cap = CaptureManager(source)

    while 1:
        frame = cap.read()

        if not cap.is_good:
            break

        cap.show(frame)

        if not cap.control():
            break
