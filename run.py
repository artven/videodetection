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
from src.detect import Detector, draw_vehicles
from src.follow import Follower
from src.classify import Classyfication
from src.logs import Database, ImageSaver

video = VideoReader(f5)
input_widnow = Window()
results = []
db = Database()
img_saver = ImageSaver()

while not key_pressed():

    frame = Frame(video)

    if not video.is_good():
        break

    vehicles, mask = Detector.find_vehicles(frame)
    objects = Follower.update(vehicles, frame, mask)

    frame = draw_vehicles(frame, vehicles)
    frame = Detector.draw_detection_region(frame)
    input_widnow.show(frame.img)

    if objects is not None:
        for obj in objects:
            res = Classyfication.perform(obj)
            results.append(res)

for record in results:
    db.write(record)
    img_saver.write(record)

logs = db.read_logs()
print(logs)

