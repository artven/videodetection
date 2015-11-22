__author__ = 'rafal'

from src.detect import Vehicle, Detector
from src.video import Frame


class ObjectRecord:
    """
    Klasa przechowująca dane o wykrytm obiekcie.
    """

    def __init__(self, new_car: Vehicle, old_car: Vehicle, new_frame: Frame, old_frame: Frame, mask):
        self.new_car, self.old_car, self.new_frame, self.old_frame, self.mask = \
            new_car, old_car, new_frame, old_frame, mask

    def unpack(self):
        return self.new_car, self.old_car, self.new_frame, self.old_frame, self.mask


class Follower:
    """
    Klasa śledząca pojazdy na kolejnych klatkach obrazu.
    """

    distance_from_border = 50

    direction = "right2left"  # "right2left"

    __tracked = []
    __detected_right = False
    __detected_left = False
    __left_lock = False
    __right_lock = False
    __frame_width = 0
    __border = 0

    @staticmethod  # TODO tę klasę należy poważnie zrefaktoryzować
    def update(new_vehicles, frame: Frame, mask):

        if len(new_vehicles) == 0:
            return None

        # Pobierz granicę detekcji.
        Follower.__border = Detector.horizontal_border

        # Zdefiniuj długość ramki.
        height, width = frame.size()
        Follower.__frame_width = width

        result = []

        Follower.__detected_left = False
        Follower.__detected_right = False

        if Follower.direction == "right2left":
            for newCar in new_vehicles:
                # detekcja z prawej strony
                if Follower.__is_on_right(newCar):
                    Follower.__detected_right = True
                    if not Follower.__right_lock:
                        Follower.__tracked.append((newCar, frame))
                        Follower.__right_lock = True
                # detekcja z lewej strony
                elif Follower.__is_on_left(newCar):
                    Follower.__detected_left = True
                    if not Follower.__left_lock:
                        Follower.__left_lock = True
                        # pobierz ze stosu pojazd
                        if len(Follower.__tracked):
                            oldCar, oldframe = Follower.__tracked.pop()
                            record = ObjectRecord(newCar, oldCar, frame, oldframe, mask)
                            result.append(record)
        elif Follower.direction == "left2right":
            for newCar in new_vehicles:
                # detekcja z lewej strony
                if Follower.__is_on_left(newCar):
                    Follower.__detected_left = True
                    if not Follower.__left_lock:
                        Follower.__tracked.append((newCar, frame))
                        Follower.__left_lock = True
                elif Follower.__is_on_right(newCar):
                    Follower.__detected_right = True
                    if not Follower.__right_lock:
                        Follower.__right_lock = True
                        # pobierz ze stosu pojazd
                        if len(Follower.__tracked):
                            oldCar, oldframe = Follower.__tracked.pop()
                            record = ObjectRecord(newCar, oldCar, frame, oldframe, mask)
                            result.append(record)

        if Follower.__detected_right is False and Follower.__right_lock is True:
            Follower.__right_lock = False

        if Follower.__detected_left is False and Follower.__left_lock is True:
            Follower.__left_lock = False

        return result if len(result) else None


    @staticmethod
    def __is_on_left(new_car):
        return new_car.centerx < (Follower.__border + Follower.distance_from_border)

    @staticmethod
    def __is_on_right(new_car):
        return new_car.centerx > (Follower.__frame_width - Follower.__border - Follower.distance_from_border)
