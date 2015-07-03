__author__ = 'rafal'

import cv2

class WriteManager:

    def __init__(self, fourcc=None, videoformat="avi", fps=20, size=(640, 480), filename=None):

        self.__forucc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        self.__format = videoformat
        self.__size = size
        self.__fps = fps

        if filename is None:
            from datetime import datetime
            td = datetime.now()
            self.__filename = "{0} {1} {2} {3}:{4}".format(td.year, td.month, td.day, td.hour, td.minute) + "." + self.__format
        else:
            self.__filename = filename + "." + self.__format

        self.__writer = cv2.VideoWriter(self.__filename, self.__forucc, self.__fps, self.__size)

    def __del__(self):
        self.__writer.release()

    def write(self, frame):
        if self.is_opened:
            self.__writer.write(frame)

    def stop_recording(self):
        self.__writer = cv2.VideoWriter.release()

    def start_recording(self, filename=None):
        if filename is None:
            from datetime import datetime
            td = datetime.now()
            self.__filename = "{0} {1} {2} {3}:{4}".format(td.year, td.month, td.day, td.hour, td.minute) + "." + self.__format
        else:
            self.__filename = filename

        self.__writer.open(self.__filename, self.__forucc, self.__fps, self.__size)

    @property
    def is_opened(self):
        return self.__writer.isOpened()

if __name__ == "__main__":
    from managers.capture import CaptureManager

    source = 0
    inputVideo = CaptureManager(source)
    outputVideo = WriteManager()

    while 1:

        frame = inputVideo.read()

        if not inputVideo.is_good:
            break

        inputVideo.show(frame)

        outputVideo.write(frame)

        if not inputVideo.control():
            break


    print("WriteManager")