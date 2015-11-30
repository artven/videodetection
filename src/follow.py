__author__ = 'rafal'

try:
    from src.detect import Vehicle, Detector
    from src.video import Frame
    from src.logs import Logger
    from src.config import Configuration
except ImportError:
    from detect import Vehicle, Detector
    from video import Frame
    from logs import Logger
    from config import Configuration

import numpy as np

class ObjectRecord:
    """
    Klasa przechowująca dane o wykrytm obiekcie.
    """

    def __init__(self, new_car: Vehicle, old_car: Vehicle, new_frame: Frame, old_frame: Frame, mask):
        self.new_car, self.old_car, self.new_frame, self.old_frame, self.mask = \
            new_car, old_car, new_frame, old_frame, mask

    def unpack(self):
        """
        Rozpakowywuje rekord.
        """

        return self.new_car, self.old_car, self.new_frame, self.old_frame, self.mask


class Follower:
    """
    Klasa śledząca pojazdy na kolejnych klatkach obrazu.
    """

    __tracked_left = []
    __tracked_right = []
    __detected_right = False
    __detected_left = False
    __left_lock = False
    __right_lock = False
    __frame_width = 0
    __border = 0

    @staticmethod
    def clear():
        """
        Czyści wewnętrzne dane algorytmu śledzenia pojazdów.
        """
        if len(Follower.__tracked_left) or len(Follower.__tracked_right):
            Logger.warning("Usunięto niewykorzystane dane.")


    @staticmethod
    def update(new_vehicles: list, frame: Frame, mask: np.ndarray):
        """
        Aktualizuje śledzone pojazdy.

        :param new_vehicles: Nowe pojazdy.
        :param Frame frame: Klatka obrazu.
        :param np.ndarray mask: Binarna maska obrazu
        :return: Zidentyfikowane pojazdy(?), None jeśli żadnego nie wykryto.
        :rtype: list
        """

        if len(new_vehicles) == 0:
            return None

        # Pobierz szerokość obrazu.
        _, Follower.__frame_width = frame.size()

        result = []

        Follower.__detected_left = False
        Follower.__detected_right = False

        if len(new_vehicles) > 1:
            Logger.warning("Otrzymano więcej niż jeden pojazd.")

        for new_car in new_vehicles:
            # detekcja z prawej strony
            if Follower.__is_on_right(new_car):
                Follower.__detected_right = True
                if not Follower.__right_lock:
                    Follower.__right_lock = True
                    # jeżeli nie ma nic po drugiej stronie to odłóż na stos
                    if not len(Follower.__tracked_left):
                        Follower.__tracked_right.append((new_car, frame))
                        Logger.info("Obiekt zarejestrwany po prawej stronie.")
                    # jeżeli bo drugiej stronie coś było to pobierz ze stosu
                    else:
                        old_car, oldframe = Follower.__tracked_left.pop()
                        record = ObjectRecord(new_car, old_car, frame, oldframe, mask)
                        Logger.info("Wykryto przejazd samochodu.")
                        result.append(record)
            # detekcja z lewej strony
            elif Follower.__is_on_left(new_car):
                Follower.__detected_left = True
                if not Follower.__left_lock:
                    Follower.__left_lock = True
                    # jeżeli nie ma nic po drugiej stronie to odłóż na stos
                    if not len(Follower.__tracked_right):
                        Follower.__tracked_left.append((new_car, frame))
                        Logger.info("Obiekt zarejestrwany po lewej stronie.")
                    # jeżeli bo drugiej stronie coś było to pobierz ze stosu
                    else:
                        old_car, oldframe = Follower.__tracked_right.pop()
                        record = ObjectRecord(new_car, old_car, frame, oldframe, mask)
                        Logger.info("Wykryto przejazd samochodu.")
                        result.append(record)

        Follower.__check_locks()

        return result if len(result) else None


    @staticmethod
    def __is_on_left(new_car: Vehicle):
        """
        Sprawdza czy samochód jest blisko lewej krawędzi obszaru czułości.

        :param Vehicle new_car: Obserwoway samochód.
        :return: Prawda/fałsz.
        :rtype: bool
        """

        hborder = Configuration.horizontal_border()
        distance = Configuration.distance_from_border()
        return new_car.centerx < (hborder + distance)

    @staticmethod
    def __is_on_right(new_car):
        """
        Sprawdza czy samochód jest blisko prawej krawędzi obszaru czułości.

        :param Vehicle new_car: Obserwoway samochód.
        :return: Prawda/fałsz.
        :rtype: bool
        """

        hborder = Configuration.horizontal_border()
        distance = Configuration.distance_from_border()
        return new_car.centerx > (Follower.__frame_width - hborder - distance)

    @staticmethod
    def __check_locks():
        """
        Sprawdza flagi detekcji i je odblokowywuje.
        """

        if Follower.__detected_right is False and Follower.__right_lock is True:
            Follower.__right_lock = False

        if Follower.__detected_left is False and Follower.__left_lock is True:
            Follower.__left_lock = False