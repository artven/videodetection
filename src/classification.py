__author__ = 'rafal'

from src.follow import ObjectRecord
from src.colordet import ColorDetector
from src.speed import SpeedMeasurment
from src.size import SizeMeasurment


class Classyfication:

    @staticmethod
    def perform(obj: ObjectRecord):
        """
        Przeprowadza ocenę koloru, rozmiaru i prędkości obiektu.
        :param obj: Obiekt wykryty przez klasę Follower.
        :return: Słownik opisujący pojazd.
        """

        # Pobierz dane o pojeździe.
        newCar, oldCar, newFrame, oldFrame, mask = obj.new_car, obj.old_car, obj.new_frame, obj.old_frame, obj.mask

        # Wybierz rejon obrazu:
        x, y, w, h = newCar.get_coordinates()
        image = newFrame.img
        roi = image[y:y+h, x:x+w, :]
        maskRoi = mask[y:y+h, x:x+w]

        # Wyznaczenie rozmiaru
        carWidth = SizeMeasurment.calculateWidth(newCar)
        carHeight = SizeMeasurment.calculateHeight(newCar)
        carArea = SizeMeasurment.calculateArea(newCar, maskRoi)

        # Wyznaczenie kolorów
        colorBar, color = ColorDetector.findColor(roi)

        # Wyznaczenie prędkości.
        speed = SpeedMeasurment.calculateSpeed(newCar, newFrame, oldCar, oldFrame)

        # Narysowanie wyników na obrazie
        # TODO nalezy poprawic podpisywanie obrazku
        image = SizeMeasurment.drawSizeInfo(image, newCar, carWidth, carHeight, carArea)
        image = ColorDetector.drawColorBar(image, colorBar)
        image = SizeMeasurment.drawCarContour(image, newCar, mask)
        image = SpeedMeasurment.drawSpeedInfo(newCar, speed, image)

        date = newFrame.creationTime

        result = {"width": carWidth, "height": carHeight, "area": carArea, "speed": speed, "image": image,
                  "date": date}

        return result

