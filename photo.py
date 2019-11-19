from matplotlib.patches import Rectangle
from point2D import Point2D
import curve
from itertools import combinations
import math


class Photo:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.name = None
        self.position = None
        self.shape = None
        self.__tl = None
        self.__tr = None
        self.__br = None
        self.__bl = None

    def get_corners(self):
        return [self.__tl, self.__tr, self.__br, self.__bl]

    @property
    def bl(self):
        return self.__bl

    @bl.setter
    def bl(self, value):
        self.__bl = value
        self.__tl = Point2D(self.bl.x, self.bl.y + self.height)
        self.__tr = Point2D(self.bl.x + self.width, self.bl.y + self.height)
        self.__br = Point2D(self.bl.x + self.width, self.bl.y)
        self.shape = Rectangle((self.bl.x, self.bl.y), self.width, self.height, fill=False)

    def overlap_with(self, other):
        other_corners = other.get_corners()
        other_tr = other_corners[1]
        other_bl = other_corners[3]
        if other_tr.x < self.__bl.x or other_bl.y > self.__tr.y or other_bl.x > self.__tr.x or other_tr.y < self.__bl.y:
            return False

        return True

    def close_enough(self, other, space):
        other_corners = other.get_corners()
        tr = other_corners[1]
        bl = other_corners[3]

        if self.__bl.x >= tr.x:
            distance = round(math.fabs(tr.x - self.__bl.x), 6)
        elif self.__tr.y <= bl.y:
            distance = round(math.fabs(bl.y - self.__tr.y), 6)
        elif self.__tr.x <= bl.x:
            distance = round(math.fabs(bl.x - self.__tr.x), 6)
        elif self.__bl.y >= tr.y:
            distance = round(math.fabs(tr.y - self.__bl.y), 6)
        else:
            raise AssertionError

        return distance >= space

    def is_in_curve(self):
        for point in self.get_corners():
            if not curve.is_point_in_curve(point):
                return False
        return True

    def clear_coords(self):
        self.shape = None
        self.__tl = None
        self.__tr = None
        self.__br = None
        self.__bl = None

    def get_indexes(self):
        """ Returns the indexes the given photo crosses in the plan. """

        corners = self.get_corners()
        keys = set()
        bl = corners[3]
        tr = corners[1]
        x_index_min = bl.get_x_index()
        x_index_max = tr.get_x_index()
        y_index_min = bl.get_y_index()
        y_index_max = tr.get_y_index()

        for x in range(x_index_min - 1, x_index_max + 2):
            for y in range(y_index_min - 1, y_index_max + 2):
                keys.add((x, y))

        return sorted(keys)

    def __str__(self):
        return "Photo({}, {}, {}, {})".format(self.width, self.height, self.bl, self.name)
        # return self.__repr__()

    def __repr__(self):
        return "P{}".format(self.name)
