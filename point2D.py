import math


class Point2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        left = math.pow(self.x + other.get_x(), 2)
        right = math.pow(self.y + other.get_y(), 2)
        return math.sqrt(left + right)

    def __str__(self):
        return "Point2D({}, {})".format(self.x, self.y)

    @staticmethod
    def __get_index(value: float):
        return math.floor(value)

    def get_x_index(self):
        return self.__get_index(self.x)

    def get_y_index(self):
        return self.__get_index(self.y)

