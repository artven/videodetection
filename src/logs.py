#!/usr/bin/env python3
__author__ = 'rafal'
__doc__ = "Moduł odpowiedzialny za zapis danych wynikowych do bazy danych i plików obrazu."

import os
import cv2
import sqlite3
import logging
from datetime import datetime


class ImageSaver:
    """
    Klasa zapisująca obraz zidentyfikowanego samochodu do pliku graficznego na dysku.
    """

    @staticmethod
    def write(record: dict):
        """
        Zapisuje do obrazu dane o samochodzie.

        :param dict record: Rekord danych.
        """

        date = record["date"]
        image = record["image"]

        filename = "images/" + str(date)[0:-7] + ".jpg"
        Logger.info("Zapisano obraz " + filename)
        cv2.imwrite(filename, image)


class Database:
    """
    Klasa obsługująca zapis i odczyt z bazy danych.
    """

    def __init__(self):
        self.fileName = str(datetime.now())[0:-7] + ".db"
        os.chdir("data")
        self.connection = sqlite3.connect(self.fileName)
        os.chdir("..")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE cars(id INTEGER PRIMARY KEY, width REAL, height REAL, "
                            "area REAL, speed REAL, detection_date DATE);")
        Logger.info("Stworzono bazę danych " + self.fileName)

    def write(self, record: dict):
        """
        Zapisuje informacje o pojeździe do bazy danych.

        :param dict record: Nowy rekord dla bazy.
        """

        width = record["width"]
        height = record["height"]
        area = record["area"]
        speed = record["speed"]
        date = record["date"]

        Logger.info("Zapisano rekord do bazy danych")

        # TODO sprawdzić czy przełamanie lini nie zepsuje zapisu
        self.cursor.execute("INSERT INTO cars(width, height, area, speed, detection_date) VALUES(%.2f, %.2f, %.2f, %.2f, ?);"
                            % (width, height, area, speed), (date,))
        self.connection.commit()

    def read_logs(self):
        """
        Odczytuje informacje z bazy danych.

        :return: Wszystkie rekordy z bazy(tablicy) samochodów.
        :rtype: list
        """

        self.cursor.execute("SELECT * FROM cars")
        self.connection.commit()
        rows = self.cursor.fetchall()
        return rows

    def table_info(self):
        """
        Zwraca nazwy kolumn tablicy przechowującej dane o samochodach.

        :return: Lista nazw.
        :rtype: list
        """

        self.cursor.execute("PRAGMA table_info(cars);")
        self.connection.commit()
        return self.cursor.fetchall()

    def execute(self, query: str):
        """
        Wykonuje zadaną komende na bazie danych i zwraca jej rezultat.

        :param str query: Treść zapytania.
        :return: Rezultat zapytania.
        :rtype: list
        """

        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()


class Logger:
    """
    Klasa zapisująca komunikaty programu do pliku tekstowego.
    """

    __root_logger = None

    @staticmethod
    def start():
        """
        Włącza możliwość logowania komunikatów.
        """

        log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s: %(message)s")
        logging.basicConfig(level=logging.DEBUG)

        root_logger = logging.getLogger()
        root_logger.name = ""
        file_handler = logging.FileHandler("data.log")
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)


        Logger.__root_logger = root_logger

    @staticmethod
    def info(txt: str):
        """
        Zapisuje informację.

        :param str txt: Tekst komunikatu.
        """

        Logger.__root_logger.info(txt)

    @staticmethod
    def error(txt: str):
        """
        Zapisuje błąd.

        :param str txt: Tekst komunikatu.
        """

        Logger.__root_logger.error(txt)

    @staticmethod
    def warning(txt: str):
        """
        Zapisuje ostrzerzenie.

        :param str txt: Tekst komunikatu.
        """

        Logger.__root_logger.warning(txt)

    @staticmethod
    def debug(txt):
        """
        Zapisuje wiadomość diagnostyczną.

        :param txt: Tekst komunikatu.
        """

        Logger.__root_logger.debug(txt)


if __name__ == '__main__':
    Logger.start()
    Logger.debug("debug asdasdsdsa")
    Logger.error("eeror asd")
    Logger.warning("warning asd")
    Logger.info("info sieiassdasd")