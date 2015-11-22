__author__ = 'rafal'

import cv2
import numpy as np

from src.follow import ObjectRecord
from src.detect import Vehicle, Frame
from src.contour import ContourDetector
from sklearn.cluster import KMeans


class Classyfication:
    """
    Klasa dokonująca klasyfikacji obiektu względem kryteriów.
    """

    # Odległość kalibracyjna wyrażona w pixelach.
    pixel_length = 200

    # Odległość kalibracyjna wyrażona w metrach.
    meters_length = 4

    # Flagi rysowania inforamcji na obrazie wynikowym.
    draw_size_info = True
    draw_color_bar = True
    draw_conturs = True
    draw_speed_info = True

    @staticmethod
    def perform(obj: ObjectRecord):
        """
        Przeprowadza ocenę koloru, rozmiaru i prędkości obiektu.
        :param obj: Obiekt wykryty przez klasę Follower.
        :return: Słownik parametrów pojazdu.
        """

        # Pobierz dane o pojeździe.
        new_car, old_car, new_frame, old_frame, mask = obj.unpack()

        # Wybierz rejon obrazu:
        x, y, w, h = new_car.get_coordinates()
        image = new_frame.img
        image_roi = new_frame.img[y:y+h, x:x+w, :]
        mask_roi = mask[y:y+h, x:x+w]

        # Wyznaczenie rozmiaru
        car_width = SizeMeasurment.calculate_width(new_car)
        car_height = SizeMeasurment.calculate_height(new_car)
        car_area = SizeMeasurment.calculate_area(new_car, mask_roi)

        # Wyznaczenie kolorów
        color_bar, color = ColorDetector.find_color(image_roi)

        # Wyznaczenie prędkości.
        speed = SpeedMeasurment.calculate_speed(new_car, new_frame, old_car, old_frame)

        # Narysowanie wyników na obrazie
        # Rozmiar
        if Classyfication.draw_size_info:
            image = SizeMeasurment.draw_size_info(image, car_width, car_height, car_area)
        # Kolor
        if Classyfication.draw_color_bar:
            image = ColorDetector.draw_color_bar(image, color_bar)
        # Kontur
        if Classyfication.draw_conturs:
            image = SizeMeasurment.draw_car_contour(image, new_car, mask)
        # Prędkość
        if Classyfication.draw_speed_info:
            image = SpeedMeasurment.draw_speed_info(new_car, speed, image)

        # Rekord zawierający informacje o pojeździe
        result = {"width": car_width, "height": car_height, "area": car_area, "speed": speed, "image": image,
                  "date": new_frame.creationTime}

        return result

    @staticmethod
    def get_ratio():
        """
        Oblicza stosunek długości na obrazie wyrażonej w pixelach do rzeczywistej długości w metrach.
        :return: Znaleziony stosunek.
        """

        return float(Classyfication.meters_length) / float(Classyfication.pixel_length)

    @staticmethod
    def draw_speed_region(frame: Frame):
        """
        Rysuje na obrazie dwie pionowe linie, służące pomiarowi osiąganej prędkości.
        :param frame: Ramka obrazu wideo.
        :return: Ramka z narysowanymi liniami.
        """

        h, w = frame.size()
        x = int(w/2) - int(Classyfication.pixel_length/2)
        frame.img = cv2.line(frame.img, (x, 0), (x, h), (255, 0, 255), thickness=4)
        frame.img = cv2.line(frame.img, (w-x, 0), (w-x, h), (255, 0, 255), thickness=4)
        return frame


class SpeedMeasurment:
    """
    Klasa dokonująca pomiaru prędkości.
    """

    @staticmethod
    def calculate_speed(new_car: Vehicle, new_frame: Frame, old_car: Vehicle, old_frame: Frame):
        """
        Oblicza prędkość wykretego pojazdu.
        :param new_car: Samochód opuszczający w pole detekcji.
        :param new_frame: Ramka obrazu przechwycona podczas opuszczania przez pojazd pola detekcji.
        :param old_car: Samochód wjeżdżający w pole detekcji.
        :param old_frame: Ramka obrazu przechwycona podczas wjeżdżania przez pojazd w pole detekcji.
        :return: Prędkość samochodu w metrach na sekundę.
        """

        time_difference = None

        # Jeżeli ramka pochodzi z pliku wideo, różnica jest obliczana na podstawie jej numeru i fps-ów.
        if not new_frame.is_from_camera:
            frame_difference = float(abs(new_frame.framePos - old_frame.framePos))
            time_difference = frame_difference * float(1/new_frame.fps)
        else:
            # Jeżeli ramka pochodzi z kamery, różnica jest obliczana na podstawie czasu jej pobrania.
            # TODO zrobić odejmowanie czasu
            return 0

        pixel_difference = float(abs(new_car.centerx - old_car.centerx))
        ratio = Classyfication.get_ratio()
        meters_difference = ratio * pixel_difference
        speed = round(meters_difference / time_difference, 5) * 3.6

        return speed

    @staticmethod
    def draw_speed_info(car: Vehicle, speed, img):
        """
        Podpisuje obraz samochodu informacją o jego prędkości
        :param car: Zidentyfikowany pojazd.
        :param speed: Obliczona prędkość.
        :param img: Obraz pojazdu.
        :return: Obraz podpisany informacją o prędkości.
        """

        # Pobierz położenie pojazdu:
        x, y, w, h = car.get_coordinates()

        text = ("S: %.2f" % speed) + " km/h"
        h, w, _ = img.shape
        org = (w - 200, h-20)
        cv2.putText(img, text, org, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 0, 0))
        return img


class SizeMeasurment:
    # Klasa dokonująca pomiaru rozmiaru samochodu.

    @staticmethod
    def calculate_width(car: Vehicle):
        """
        Wylicza szerokość(długość) samochodu w metrach.
        :param car: Obiekt reprezenetujący samochód.
        :return: Szerkość wyrażona w metrach.
        """

        width = car.w
        ratio = Classyfication.get_ratio()
        return width * ratio

    @staticmethod
    def calculate_height(car: Vehicle):
        """
        Wylicza wysokośc samochodu w metrach.
        :param car: Obiekt reprezenetujący samochód.
        :return: Wysokość wyrażona w metrach.
        """

        height = car.h
        ratio = Classyfication.get_ratio()
        return height * ratio

    @staticmethod
    def calculate_area(mask):
        """
        Oblicza pole powierzchni bocznej obiektu. Rozmiar obiektu jest obliczna na podstawie ilosci pixeli obiektu
        razy przelicznik pixele na metry.
        :param mask: Binarna maska obrazu.
        :return: Pole powierzchni bocznej karoserii pojazdu.
        """

        # Znajdź kontury samochodu.
        contours = ContourDetector.find(mask)

        # Wyszkuaj kontur o największym polu.
        cnt = SizeMeasurment.__find_biggest_contour(contours)

        # Oblicz pole konturu.
        area = ContourDetector.area(cnt)
        ratio = Classyfication.get_ratio()
        area = round(area*ratio*ratio, 2)

        return area

    @staticmethod
    def draw_car_contour(img, car, bin_mask):
        """
        Rysuje kontur samochodu na obrazie.
        :param img: Obraz samochodu.
        :param car: Obiekt reprezentujący pojazd.
        :param bin_mask: Binarna maska obrazu.
        :return: Obraz z oznaczonym konturem samochodu.
        """

        # Wyznacz rejon pojazdu na obrazie.
        x, y, w, h = car.get_coordinates()
        mask = bin_mask[y:y+h, x:x+w]
        image = img[y:y+h, x:x+w, :]

        # Znajdź kontury samochodu.
        contours = ContourDetector.find(mask)

        # Wyszkuaj kontur o największym polu.
        cnt = SizeMeasurment.__find_biggest_contour(contours)
        image = ContourDetector.draw(image, cnt, (255, 0, 0), thickness=2)
        img[y:y+h, x:x+w, :] = image
        return img

    @staticmethod
    def draw_size_info(img, car_width, car_height, car_area):
        """
        Podpisuje obraz samochodu jego wymiarami.
        :param img: Obraz samochodu.
        :param car_width: Szerokość(długość) samochodu.
        :param car_height: Wysokość samochodu.
        :param car_area: Pole powierzchni bocznej pojazdu.
        :return: Podpisany parametrami pojadu obraz.
        """

        text = "width=%.2f m, height=%.2f m, area=%.2f m2" % (car_width, car_height, car_area)
        h, w, _ = img.shape
        text_place = (0, h-20)
        cv2.putText(img, text, text_place, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 0, 0))

        return img

    @staticmethod
    def __find_biggest_contour(contours):
        """
        Wybiera z konturów ten o największej powierzchni.
        :param contours: Hierarchia konturów.
        :return: Największy znaleziony kontur.
        """

        if len(contours) > 1:
            max_area, contour_index = ContourDetector.area(contours[0]), 0
            for index in range(len(contours)):
                area = ContourDetector.area(contours[index])
                if area > max_area:
                    max_area, contour_index = area, index
            cnt = contours[contour_index]
            return cnt
        elif len(contours) == 1:
            # TODO nie wiem czy ma być index
            return contours[0]
        else:
            return None


# Przy implementacji modułu skorzystano z materiałów:
# http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# http://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

class ColorDetector:
    # Klasa określająca kolor pojazdu.

    # Liczba kolorów wyszukiwanych w obrazie.
    color_number = 5

    # Wysokość i szerokość zwracanego obrazu z konsoli.
    __bar_height = 50
    __bar_width = 300

    @staticmethod
    def __centroid_histogram(clt):
        """
        Przydziala wartości histogramu do zdefiniowanych grup. Dokonuje normalizacji nowego histogramu.
        :param clt: Zdefiniowane przez KMeans grupy.
        :return: Histogram po przydziale pikseli.
        """

        # Przydziel piksele względem grup.
        num_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=num_labels)

        # Znormalizuj histogram.
        hist = hist.astype("float")
        hist /= hist.sum()

        # Zwróć nowy histogram.
        return hist

    @staticmethod
    def __find_dominant_colors(image, n):
        """
        Znajduje n najbardziej dominujących kolorów na obrazie.
        :param image: badany obraz.
        :param n: liczba poszukiwanych kolorów.
        :return: lista znalezionych kolorów, procent powierzni kolorów.
        """

        # Przekształć obraz w listę pixeli.
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        # Podziel obraz na grupy.
        clt = KMeans(n_clusters=n)
        clt.fit(image)

        # Oblicz histogram nowego obrazu.
        hist = ColorDetector.__centroid_histogram(clt)

        # Dokonaj konwersji i zaokrąglenia wyników.
        percents = hist
        colors = clt.cluster_centers_  # BGR

        color_bar = ColorDetector.__create_colors_bar(hist, clt.cluster_centers_)

        result_colors = []
        result_percents = []

        for col in colors:
            result_colors.append(((int(col[0])), int(col[1]), int(col[2])))
        for pen in percents:
            result_percents.append(round(pen, 3))

        return result_colors, result_percents, color_bar

    @staticmethod
    def __create_colors_bar(hist, centroids):
        """
        Tworzy pasek zawierający najpopularniejsze kolory.
        :param hist: Histogram obrazu.
        :param centroids: Liczba poszukiwanych kolorów.
        :return:
        """

        # TODO ogarnąć co to są centroids ???
        w = ColorDetector.__bar_width
        h = ColorDetector.__bar_height

        # Pusty, zainicjowany pasek.
        bar = np.zeros((h, w, 3), dtype=np.uint8)
        startx = 0

        # Sprawdź dla każdego koloru.
        for (percent, color) in zip(hist, centroids):
            endx = startx + (percent * 300)
            cv2.rectangle(bar, (int(startx), 0), (int(endx), 50),
            color.astype("uint8").tolist(), -1)
            startx = endx

        return bar

    @staticmethod
    def find_color(image):
        """
        Przeprowadza analizę dominujących kolorów, wybiera z nich największy.
        :param image: przeszukiwany obraz.
        :return: obraz wypełniony kolorem, wartość koloru.
        """

        # Znajdź najlepsze kolory.
        colors, percents, color_bar = ColorDetector.__find_dominant_colors(image, n=int(ColorDetector.color_number))

        # Wybierz największy kolor.
        best_percent = max(percents)
        best_percent_index = percents.index(best_percent)
        color = colors[best_percent_index]

        return color_bar, color

    @staticmethod
    def draw_color_bar(img, color_bar):
        width = ColorDetector.__bar_width
        height = ColorDetector.__bar_height
        img[:height, :width, :] = color_bar
        return img
