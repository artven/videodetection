__author__ = 'rafal'

from src.detect import Detector, draw_vehicles
from src.video import Frame
from src.follow import Follower
from src.config import Configuration
from src.classify import Classyfication
import cv2

class Algorithm:
    """
    Klasa opakowywująca algorytm przetwarzania obrazu z kamery.
    """

    file = ""

    @staticmethod
    def set_file(file_path):
        """
        Ustawia ścieżkę przetwarzanego pliku.
        """

        Algorithm.file = file_path

    @staticmethod
    def reset():
        """
        Usuwane dane przechowywane przez algorytm.
        """

        Follower.clear()

    @staticmethod
    def resize(frame: Frame):
        """
        Zmienia rozmiar obrazu na (720, 480).

        :return: Klatka obrazu o zmienionym rozmiarze.
        :rtype: Frame
        """

        frame.img = cv2.resize(frame.img, (720, 480))

        return frame

    @staticmethod
    def perform(frame: Frame, database, img_saver, run_classyfication=True):
        """
        Dokonuje przetwarzania ramki obrazu przez algorytm.

        :param frame: Ramka obrazu.
        :param database: Baza danych do zapisywania parametrów.
        :param img_saver: Obiekt zapisyjący pliki obrazów.
        :return: Przetworzona ramka.
        """

        vehicles, mask = Detector.find_vehicles(frame)
        objects = Follower.update(vehicles, frame, mask)

        records = []

        if run_classyfication:
            if objects is not None:
                for obj in objects:
                    record = Classyfication.perform(obj)
                    records.append(record)
                    database.write(record, Algorithm.file)
                    img_saver.write(record)

        # Rysowanie pojazdów.
        if Configuration.draw_cars():
            frame = draw_vehicles(frame, vehicles)

        # Rysowanie obszaru wykrywania.
        if Configuration.draw_detection_region():
            frame = Detector.draw_detection_region(frame)

        # Rysowanie obszaru pomiaru prędkości
        if Configuration.draw_speed_region():
            frame = Classyfication.draw_speed_region(frame)

        return frame, mask, records
