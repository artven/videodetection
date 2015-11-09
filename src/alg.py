__author__ = 'rafal'

from src.detect import Detector
from src.detect import draw_vehicles
from src.video import Frame
from src.follow import Follower
from src.config import Configuration
from src.classify import Classyfication


def perform(frame: Frame, database, img_saver):

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

    if Configuration.run_alg:
        if objects is not None:
            for obj in objects:
                record = Classyfication.perform(obj)
                database.write(record)
                img_saver.write(record)

    return frame
