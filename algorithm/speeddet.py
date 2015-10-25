__author__ = 'rafal'

class SpeedMeasurment:
    # Klasa dokonująca pomiaru rozmiaru samochodu.

    # Odległość w pikselach.
    __pixelLength = 200

    # Odległość rzeczywista w metrach.
    __metersLength = 4

    # Interfejs klasy.

    @staticmethod
    def calculateSpeed(newCar, frame, oldCar, oldframe):

        timeDiff = None

        # Jeżeli ramka pochodzi z pliku wideo, różnica jest obliczana na podstawie jej numeru.
        if frame.isFromCamera() and oldframe.isFromCamera():
            frameCount = float(abs(frame.frameNr - oldframe.frameNr))
            timeDiff = frameCount * float(1/frame.getFPS())
        else:
            # Jeżeli ramka pochodzi z kamery, różnica jest obliczana na podstawie czasu jej pobrania.
            pass

        pixelDiff = float(abs(newCar.centerx - oldCar.centery))
        ratio = SpeedMeasurment.__getRatio()
        metersDiff = ratio * pixelDiff
        speed = round(metersDiff / timeDiff)
        return speed

    # Funkcje pomocnicze.

    @staticmethod
    def __getRatio():
        meters = SpeedMeasurment.__metersLength
        pixels = SpeedMeasurment.__pixelLength
        ratio = float(meters) / pixels
        return ratio
