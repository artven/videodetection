__author__ = 'rafal'

from datetime import datetime

from algorithm.objects import Vehicle


class LogWriter:


    def __init__(self):
        datetime.now().
        self.fileName = (datetime.now()).replace(".", ":") + ".log"
        self.file = open(self.fileName)


    def write(self, vehicles):
        for veh in vehicles:
            pass



class Record:
    pass