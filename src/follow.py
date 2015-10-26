__author__ = 'rafal'

# from algorithm.contourdet import ContourDetector
from src.detect import Vehicle
from src.video import Frame
from src.detect import Detector


class ObjectRecord:
    # Klasa przechowująca dane o wykrytm obiekcie

    def __init__(self, new_car: Vehicle, old_car: Vehicle, new_frame: Frame, old_frame: Frame, mask):
        self.new_car, self.old_car, self.new_frame, self.old_frame, self.mask = \
            new_car, old_car, new_frame, old_frame, mask


class Follower:

    tracked = []

    distanceFromBorder = 50

    direction = "right2left"  # "right2left"

    detectedCarOnRight = False
    detectedCarOnLeft = False
    leftLock = False
    rightLock = False


    @staticmethod
    def update(newVehicles, frame: Frame, mask):

        # Pobierz granicę detekcji.
        border = Detector.verticalBorder

        # Zdefiniuj długość ramki.
        height, width = frame.size()
        frame_width = width


        result = []

        Follower.detectedCarOnLeft = False
        Follower.detectedCarOnRight = False

        if Follower.direction == "right2left":
            for newCar in newVehicles:
                # detekcja z prawej strony
                if Follower.isCloseToRightBorder(newCar):
                    Follower.detectedCarOnRight = True
                    if not Follower.rightLock:
                        Follower.tracked.append((newCar, frame))
                        Follower.rightLock = True
                        # print("nowy obiekt z prawej")
                # detekcja z lewej strony
                elif Follower.isCloseToLeftBorder(newCar):
                    Follower.detectedCarOnLeft = True
                    if not Follower.leftLock:
                        Follower.leftLock = True
                        # print("nowy obiekt z lewej")
                        # pobierz ze stosu pojazd
                        if len(Follower.tracked):
                            oldCar, oldframe = Follower.tracked.pop()
                            record = ObjectRecord(newCar, oldCar, frame, oldframe, mask)
                            result.append(record)
                            # print("Nowy obiekt!")
                        else:
                            # print("Nie udało się pobrać danych o obiekcie!")
                            pass
        elif Follower.direction == "left2right":
            for newCar in newVehicles:
                # detekcja z lewej strony
                if Follower.isCloseToLeftBorder(newCar):
                    Follower.detectedCarOnLeft = True
                    if not Follower.leftLock:
                        Follower.tracked.append((newCar, frame))
                        Follower.leftLock = True
                        # print("nowy obiekt z lewej")
                elif Follower.isCloseToRightBorder(newCar):
                    Follower.detectedCarOnRight = True
                    if not Follower.rightLock:
                        Follower.rightLock = True
                        # print("nowy obiekt z prawej")
                        # pobierz ze stosu pojazd
                        if len(Follower.tracked):
                            oldCar, oldframe = Follower.tracked.pop()
                            record = ObjectRecord(newCar, oldCar, frame, oldframe, mask)
                            result.append(record)
                            print("Nowy obiekt!")
                        else:
                            pass
                            # print("Nie udało się pobrać danych o obiekcie!")

        if Follower.detectedCarOnRight is False and Follower.rightLock is True:
            # print("zdjęto blokadę z prawej!")
            Follower.rightLock = False

        if Follower.detectedCarOnLeft == False and Follower.leftLock==True:
            # print("zdjęto blokadę z lewej!")
            Follower.leftLock = False

        return result if len(result) else None


    @staticmethod
    def isCloseToLeftBorder(newCar):
        return newCar.centerx < (Follower.border + Follower.distanceFromBorder)

    @staticmethod
    def isCloseToRightBorder(newCar):
        return newCar.centerx > (Follower.frameWidth - Follower.border - Follower.distanceFromBorder)
