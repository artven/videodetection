__author__ = 'rafal'


from src.detect import Detector
from src.follow import Follower
from src.classify import Classyfication
from src.classify import ColorDetector

import json


class Configuration:
    filename = "config.json"

    __default_config = {
        "pixel_length": 200,
        "meters_length": 4,
        "color_number": 5,
        "horizontal_border": 200,
        "vertical_border": 50,
        "pixel_limit": 1000,
        "direction":  "left2right",
        "distance_from_border": 50,
        "draw_detection_region": True,
        "draw_speed_region": True,
        "draw_cars": True,
        "draw_conturs": True,
        "draw_speed_info": True,
        "draw_size_info": True,
        "draw_color_bar": True
        }

    __current_config = {}

    __draw_detection_region = True
    __draw_speed_region = True
    __draw_cars = True

    @staticmethod
    def laod_config(file=filename):
        with open(file) as data_file:
            Configuration.__current_config = json.load(data_file)
        Configuration.__write_all()

    @staticmethod
    def save_config(file=filename):
        Configuration.__load_all()
        with open(file, 'w') as outfile:
            json.dump(Configuration.__current_config, outfile)


    @staticmethod
    def restore_default(file=filename):
        Configuration.__current_config = Configuration.__default_config.copy()
        with open(file, 'w') as outfile:
            json.dump(Configuration.__current_config, outfile)
        Configuration.__write_all()

    @staticmethod
    def __load_all():

        Configuration.__current_config["pixel_length"] = Configuration.pixel_length()
        Configuration.__current_config["meters_length"] = Configuration.meters_length()
        Configuration.__current_config["color_number"] = Configuration.color_number()
        Configuration.__current_config["horizontal_border"] = Configuration.horizontal_border()
        Configuration.__current_config["vertical_border"] = Configuration.vertical_border()
        Configuration.__current_config["pixel_limit"] = Configuration.pixel_limit()
        Configuration.__current_config["direction"] = Configuration.direction()
        Configuration.__current_config["distance_from_border"] = Configuration.distance_from_border()
        Configuration.__current_config["draw_detection_region"] = Configuration.draw_detection_region()
        Configuration.__current_config["draw_speed_region"] = Configuration.draw_speed_region()
        Configuration.__current_config["draw_cars"] = Configuration.draw_cars()
        Configuration.__current_config["draw_conturs"] = Configuration.draw_conturs()
        Configuration.__current_config["draw_speed_info"] = Configuration.draw_speed_info()
        Configuration.__current_config["draw_size_info"] = Configuration.draw_size_info()
        Configuration.__current_config["draw_color_bar"] = Configuration.draw_color_bar()

    @staticmethod
    def __write_all():

        config = Configuration.__current_config

        Configuration.pixel_length(config["pixel_length"])
        Configuration.meters_length(config["meters_length"])
        Configuration.color_number(config["color_number"])
        Configuration.horizontal_border(config["horizontal_border"])
        Configuration.vertical_border(config["vertical_border"])
        Configuration.pixel_limit(config["pixel_limit"])
        Configuration.direction(config["direction"])
        Configuration.distance_from_border(config["distance_from_border"])
        Configuration.draw_detection_region(config["draw_detection_region"])
        Configuration.draw_speed_region(config["draw_speed_region"])
        Configuration.draw_cars(config["draw_cars"])
        Configuration.draw_conturs(config["draw_conturs"])
        Configuration.draw_speed_info(config["draw_speed_info"])
        Configuration.draw_size_info(config["draw_size_info"])
        Configuration.draw_color_bar(config["draw_color_bar"])


    # Opcje konfiguracji programu:

    @staticmethod
    def pixel_length(value=None):
        if value is not None:
            Classyfication.pixel_length = value
        return Classyfication.pixel_length

    @staticmethod
    def meters_length(value=None):
        if value is not None:
            Classyfication.meters_length = value
        return Classyfication.meters_length

    @staticmethod
    def color_number(value=None):
        if value is not None:
            ColorDetector.color_number = value
        return ColorDetector.color_number

    @staticmethod
    def horizontal_border(value=None):
        if value is not None:
            Detector.horizontal_border = value
        return Detector.horizontal_border

    @staticmethod
    def vertical_border(value=None):
        if value is not None:
            Detector.vertical_border = value
        return Detector.vertical_border

    @staticmethod
    def pixel_limit(value=None):
        if value is not None:
            Detector.pixel_limit = value
        return Detector.pixel_limit

    @staticmethod
    def direction(value=None):
        if value is not None:
            Follower.direction = value
        return Follower.direction

    @staticmethod
    def distance_from_border(value=None):
        if value is not None:
            Follower.distance_from_border = value
        return Follower.distance_from_border

    # Opcje rysowania oznaczeń:

    @staticmethod
    def draw_detection_region(value=None):
        if value is not None:
            Configuration.__draw_detection_region = value
        return Configuration.__draw_detection_region

    @staticmethod
    def draw_speed_region(value=None):
        if value is not None:
            Configuration.__draw_detection_region = value
        return Configuration.__draw_detection_region

    @staticmethod
    def draw_cars(value=None):
        if value is not None:
            Configuration.__draw_cars = value
        return Configuration.__draw_cars

    @staticmethod
    def draw_conturs(value=None):
        if value is not None:
            Classyfication.draw_conturs = value
        return Classyfication.draw_conturs

    @staticmethod
    def draw_speed_info(value=None):
        if value is not None:
            Classyfication.draw_speed_info = value
        return Classyfication.draw_speed_info

    @staticmethod
    def draw_size_info(value=None):
        if value is not None:
            Classyfication.draw_size_info = value
        return Classyfication.draw_size_info

    @staticmethod
    def draw_color_bar(value):
        if value is not None:
            Classyfication.draw_color_bar = value
        return Classyfication.draw_color_bar

if __name__ == "__main__":
    print("restore default config")
    Configuration.restore_default()

