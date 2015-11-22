__author__ = 'rafal'
__doc__ = """
Moduł odpowiedzialny za zapis danych wynikowych do bazy danych i plików obrazu.
"""

from datetime import datetime

import os
import cv2
import sqlite3


class ImageSaver:
    """
    Klasa zapisująca obraz zidentyfikowanego samochodu do pliku graficznego na dysku.
    """

    @staticmethod
    def write(record):
        """
        Zapisuje do obrazu dane o samochodzie.
        :param record: Rekord danych.
        :return:
        """

        date = record["date"]
        image = record["image"]

        filename = "images/" + str(date)[0:-7] + ".jpg"
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

    def write(self, record):
        """

        :param record: Informacje o pojeździe
        :return:
        """
        width = record["width"]
        height = record["height"]
        area = record["area"]
        speed = record["speed"]
        date = record["date"]

        # TODO dodać to do loggera
        # print("nowy obiekt w:"+str(width)+" h:"+str(height)+" a:"+str(area)+" s:"+str(speed)+" d:sub"+str(date))

        # TODO sprawdzić czy przełamanie lini nie zepsuje zapisu
        self.cursor.execute("INSERT INTO cars(width, height, area, speed, detection_date) VALUES(%.2f, %.2f, %.2f, %.2f, ?);"
                            % (width, height, area, speed), (date,))
        self.connection.commit()

    def read_logs(self):
        """
        Odczytuje informacje z bazy danych.
        :return: Wszystkie rekordy z bazy(tablicy samochodów.
        """

        self.cursor.execute("SELECT * FROM cars")
        self.connection.commit()
        rows = self.cursor.fetchall()
        return rows

    def table_info(self):
        """
        Zwraca nazwy kolumn tablicy przechowującej dane o samochodach.
        :return: Lista nazw.
        """

        self.cursor.execute("PRAGMA table_info(cars);")
        self.connection.commit()
        return self.cursor.fetchall()

    def execute(self, query):
        """
        Wykonuje zadaną komende na bazie danych i zwraca jej rezultat.
        :param query: Treść zapytania.
        :return: Rezultat zapytania.
        """

        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()



