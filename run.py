#!/usr/bin/env python3
__author__ = 'rafal'

# przypadki testowe left2right
f1 = 'videos/samples/samochód bordowy akropol.avi'
f2 = 'videos/samples/samochód srebrny akropol.avi'
f3 = 'videos/samples/samochód zielony.avi'
f4 = 'videos/samples/taksówka akropol.avi'

# przypadki testowe right2left
f5 = 'videos/vid1.avi'

from src.utilities import key_pressed
from src.video import VideoReader, Window, Frame


video = VideoReader(f5)
input_widnow = Window()

while not key_pressed():

    image = video.read()

    if not video.is_good():
        break

    input_widnow.show(image)




'''

# narzędzia pomocnicze
from utilities.keys import keypressed
from src.video import VideoReader
from utilities.frame import Frame

# algorytm
from src.core import algorithm
# from algorithm.analysis import getVehiclesData, printVehiclesData, preSelectVehicles
from src.analysis import preSelectVehicles
from src.follow import Follower
# from algorithm.classification import VehiclesClassifier
from src.classification import Classyfication



foundObjects = []

# files = [f1, f2, f3, f4]
files = [f5]

from src.logs import Logger

database = Logger()

for filename in files:

    inputVideo = VideoReader(filename)
    # outputWindow = Window()

    while not keypressed():

        frame = Frame(inputVideo)

        if not inputVideo.isGood():
            break

        vehicles, mask = algorithm(frame)
        vehicles, frame = preSelectVehicles(vehicles, frame, drawLines=False)
        objects = Follower.update(vehicles, frame, mask)

        if objects is not None:
            foundObjects.extend(objects)

        # outputWindow.show(drawObjects(frame.img, vehicles))

# print("znaleziono samochodów: " + str(len(foundObjects)))

classificationResults = []

if len(foundObjects):
    for obj in foundObjects:
        res = Classyfication.perform(obj)
        classificationResults.append(res)

for res in classificationResults:
    database.writeRecord(res)

rows = database.readLogs()

print(database.tableInfo())

for row in rows:
    print(row)

'''