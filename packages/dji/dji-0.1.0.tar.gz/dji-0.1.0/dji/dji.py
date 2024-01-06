class Dji:
    def __init__(self, gsd):
        self.__f = 8.8
        self.__pixel_size = 0.00241
        self.__gsd = gsd/100

    def calculate_flight_high(self):
        return int((self.__f * self.__gsd) / self.__pixel_size)