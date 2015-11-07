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
from src.video import VideoReader, VideoWriter, OpenCVWindow, Frame
from src.detect import Detector, draw_vehicles
from src.follow import Follower
from src.classify import Classyfication
from src.logs import Database, ImageSaver
from src.config import Configuration

Configuration.load_config()
# Configuration.pixel_length(400)
# Configuration.draw_speed_region(False)
# Configuration.draw_detection_region(False)
# Configuration.draw_conturs(False)
# Configuration.draw_size_info(False)
# Configuration.draw_speed_info(False)
# Configuration.draw_color_bar(False)

video = VideoReader(f5)
output_video = VideoWriter(video.size())
input_widnow = OpenCVWindow()
db = Database()
img_saver = ImageSaver()

results = []

while not key_pressed():

    frame = Frame(video)

    if not video.is_good():
        break

    vehicles, mask = Detector.find_vehicles(frame)
    objects = Follower.update(vehicles, frame, mask)

    # Rysowanie pojazdów.
    if Configuration.draw_cars():
        frame = draw_vehicles(frame, vehicles)

    # Rysowanie obszaru wykrywania.
    if Configuration.draw_detection_region():
        frame = Detector.draw_detection_region(frame)

    # Rysowanie obszaru pomiaru prędkości
    if Configuration.draw_speed_region():
        frame = Classyfication.draw_speed_region(frame)

    input_widnow.show(frame.img)
    output_video.write(frame.img)

    if objects is not None:
        for obj in objects:
            res = Classyfication.perform(obj)
            results.append(res)

for record in results:
    db.write(record)
    img_saver.write(record)


