__author__ = 'rafal'

import cv2
import numpy as np
from datetime import datetime


class VideoReader:
    """
    Klasa obsługująca odczyt obrazu z urządzeń oraz plików.
    """

    def __init__(self, videosource=0):
        self.source = videosource
        self.__cap = cv2.VideoCapture(self.source)
        self.__good = self.__cap.isOpened()
        self.__frame = None

    def __del__(self):
        self.__cap.release()

    def read(self):
        """
        Odczytuje ramkę obrazu wideo.

        :return: None jeśli odczyt się nie powiódł, klatka obrazu w przeciwnym wypadku.
        """

        ret, image = self.__cap.read()
        if not ret:
            self.__good = False
            return None

        return image

    def is_good(self):
        """
        Sprawdza czy źródło obrazu wideo jest sprawne.

        :return: Prawda/fałsz.
        """

        return self.__good

    def position_mseconds(self):
        """
        Zwraca pozycję w pliku wideo wyrażoną w milisekundach.

        :return: Liczba określająca pozycję.
        """

        return self.__cap.get(cv2.CAP_PROP_POS_MSEC)

    def position_frames(self):
        """
        Zwraca pozycję w pliku wideo wyrażoną w liczbie klatek.

        :return: Liczba określająca pozycję.
        """

        return self.__cap.get(cv2.CAP_PROP_POS_FRAMES)

    def fps(self):
        """
        Zwraca liczbę klatek na sekundę.

        :return: Liczba klatek na sekundę.
        """

        return self.__cap.get(cv2.CAP_PROP_FPS)

    def frames_count(self):
        """
        Zwraca liczbę klatek w pliku wideo.

        :return: Liczba klatek.
        """

        return int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def size(self):
        """
        Zwraca rozmiar klatki obrazu.

        :return: Szerokość obrazu, wysokość obrazu.
        """

        return int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


class VideoWriter:
    """
    Klasa zapisująca dane wynikowe do pliku wideo.
    """

    """ format zapisu danych     """
    forucc = cv2.VideoWriter_fourcc('M','J','P','G')
    format = ".avi"
    fps = 20
    folder = "videos/"
    size = (720, 480)

    def __init__(self):

        self.__filename = VideoWriter.folder + str(datetime.now())[0:-7] + VideoWriter.format
        self.__writer = cv2.VideoWriter(self.__filename, VideoWriter.forucc, VideoWriter.fps, VideoWriter.size)

    def __del__(self):
        self.__writer.release()

    def write(self, image: np.ndarray):
        """
        Zapisuje klatkę obrazu do pliku wideo.

        :param np.ndarray image: Zapisaywana ramka obrazu.
        """

        if self.__writer.isOpened():
            self.__writer.write(image)


class OpenCVWindow:
    """
    Klasa dostarczająca okienko pozwalające wyświetlać obraz.
    """

    __id = 0

    def __init__(self, windowmode=cv2.WINDOW_FREERATIO):
        """
        :param windowmode: Tryb zachowania okna, domyślnie
        """

        OpenCVWindow.__id += 1
        self.__name = "Window" + str(OpenCVWindow.__id)
        self.__mode = windowmode
        cv2.namedWindow(self.__name, self.__mode)

    def __del__(self):
        cv2.destroyWindow(self.__name)

    def show(self, img: np.ndarray):
        """
        Wyświetla obraz oknie.

        :param np.ndarray img: Klatka obrazu.
        """

        cv2.imshow(self.__name, img)

    def get_name(self):
        """
        Zwraca unikalną nazwę przypisaną do okna.

        :return: Nazwa okna w postaci Window+id
        :rtype: str
        """

        return self.__name


class Frame:
    """
    Klasa opakowywujacą klatkę obrazu.
    """

    def __init__(self, inputVideo: VideoReader):
        """
        :param VideoReader inputVideo: Plik źródłowy lub urządzenie z którego pobierany jest obraz.
        """

        # Sprawdź czy plik źródłowy jest podany w postaci napisu.
        # Jeśli tak, oznacza to, że został odczytany plik.
        # W przeciwynym przypadku obraz pochodzi bezpośrednio z kamery.
        if isinstance(inputVideo.source, str):
            self.is_from_camera = False
        else:
            self.is_from_camera = True

        self.img = inputVideo.read()
        if self.img is not None:
            self.orginal_img = self.img.copy()
        else:
            self.orginal_img = None
        self.creationTime = datetime.now()
        self.fps = inputVideo.fps()
        self.framePos = inputVideo.position_frames()

    def size(self):
        """
        Zwraca wysokość i szerokość obrazu.

        :return: Wysokość obrazu, szerokość obrazu.
        :rtype: tuple
        """

        # TODO ogranąć czy kolejność jest prawidłowa.
        return self.img.shape[0], self.img.shape[1]