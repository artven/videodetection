__author__ = 'rafal'

from datetime import datetime

import os
import sqlite3

class Record:
    pass


class Logger:

    def __init__(self):
        self.fileName = str(datetime.now())[0:-7] + ".db"
        os.chdir("data")
        self.connection = sqlite3.connect(self.fileName)
        os.chdir("..")
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE cars(id INTEGER PRIMARY KEY, width REAL, height REAL, "
                            "area REAL, speed REAL, detection_date DATE);")

    def writeRecord(self, record):
        width = record["width"]
        height = record["height"]
        area = record["area"]
        speed = record["speed"]
        date = record["date"]

        self.cursor.execute("INSERT INTO cars(width, height, area, speed, detection_date) VALUES(?, ?, ?, ?, ?);",
                            (width, height, area, speed, date))
        self.connection.commit()

    def readLogs(self):
        self.cursor.execute("SELECT * FROM cars")
        self.connection.commit()
        rows = self.cursor.fetchall()

        return rows

    def tableInfo(self):
        self.cursor.execute("PRAGMA table_info(cars);")
        self.connection.commit()
        return self.cursor.fetchall()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()



