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
        tmp = str(datetime.now())[0:-7].split(sep=" ")
        name = tmp[0] + "_" + tmp[1]
        self.fileName = name + ".db"
        os.chdir("data")
        self.connection = sqlite3.connect(self.fileName)
        os.chdir("..")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE cars(id INTEGER PRIMARY KEY, width REAL, height REAL, "
                            "area REAL, speed REAL, file TEXT, detection_date DATE);")
        Logger.info("Stworzono bazę danych " + self.fileName)

    def write(self, record: dict, path=""):
        """
        Zapisuje informacje o pojeździe do bazy danych.

        :param str path: Ścieżka do pliku wideo z którego pochodzą wykryte dane.
        :param dict record: Nowy rekord dla bazy.
        """

        width = record["width"]
        height = record["height"]
        area = record["area"]
        speed = record["speed"]
        date = record["date"]
        path = "\"" + path.split(sep="/")[-1] + "\""
        Logger.info("Zapisano rekord do bazy danych")

        self.cursor.execute("INSERT INTO cars(width, height, area, speed, file, detection_date) VALUES(%.2f, %.2f, %.2f, %.2f, %s, ?);"
                            % (width, height, area, speed, path), (date,))
        self.connection.commit()

    def read_all_records(self):
        """
        Odczytuje informacje z bazy danych.

        :return: Wszystkie rekordy z bazy(tablicy) samochodów.
        :rtype: list
        """

        self.cursor.execute("SELECT * FROM cars")
        self.connection.commit()
        return self.cursor.fetchall()

    @staticmethod
    def read_all_records_from_file(filepath):
        """
        Zwraca rekordy z bazy o podanej ścieżce dostępu.

        :param filepath: Ścieżka do pliku bazy danych.
        :return: Rekordy w bazie
        :rtype: list
        """

        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cars")
        connection.commit()
        return cursor.fetchall()

    def column_names(self):
        """
        Zwraca nazwy kolumn tablicy przechowującej dane o samochodach.

        :return: Lista nazw.
        :rtype: list
        """

        self.cursor.execute("PRAGMA table_info(cars);")
        self.connection.commit()
        return self.cursor.fetchall()

    @staticmethod
    def column_names_from_file(filepath):
        """
        Zwraca nazwy kolumn z bazy o podanej ścieżce dostępu.

        :param filepath:
        :return:
        """
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(cars);")
        connection.commit()
        return cursor.fetchall()

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