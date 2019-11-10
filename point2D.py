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

    def get_x_indexes_between(self, other):
        if self.x == other.x:
            return None
        else:
            x_min = min(self.get_x_index(), other.get_x_index())
            x_max = max(self.get_x_index(), other.get_x_index())
            return range(x_min, x_max + 1)

    def get_y_indexes_between(self, other):
        if self.y == other.y:
            return None
        else:
            y_min = min(self.get_y_index(), other.get_y_index())
            y_max = max(self.get_y_index(), other.get_y_index())
            return range(y_min, y_max + 1)

    def __lt__(self, other):
        """Using "reading order" in a coordinate system where 0,0 is bottom left"""
        try:
            return (-self.y, self.x) < (-other.y, other.x)
        except AttributeError:
            return NotImplemented

