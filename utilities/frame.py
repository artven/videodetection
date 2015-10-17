__author__ = 'rafal'


class Frame:
    # Klasa opakowywujacą klatkę obrazu.

    def __init__(self, img, time=None):
        self.img = img
        pass

    def isBGR(self):
        return len(self.img.shape) == 3

    def getSize(self):

        pass


    def __getCurrentDataTime(self):
        pass
    
