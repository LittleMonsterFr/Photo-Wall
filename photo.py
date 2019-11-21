from matplotlib.patches import Rectangle
from point2D import Point2D
import curve
import math


class Photo:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.name = None
        self.position = None
        self.shape = None
        self.tl = None
        self.tr = None
        self.br = None
        self.bl = None

    def update_coordinates(self, bottom_left_point):
        self.bl = bottom_left_point
        self.tl = Point2D(self.bl.x, self.bl.y + self.height)
        self.tr = Point2D(self.bl.x + self.width, self.bl.y + self.height)
        self.br = Point2D(self.bl.x + self.width, self.bl.y)
        self.shape = Rectangle((self.bl.x, self.bl.y), self.width, self.height, fill=False)

    def overlap_with(self, other):
        if other.tr.x < self.bl.x or other.bl.y > self.tr.y or other.bl.x > self.tr.x or other.tr.y < self.bl.y:
            return False

        return True

    def too_close(self, other, space):
        if self.bl.x >= other.tr.x:
            distance = round(math.fabs(other.tr.x - self.bl.x), 6)
        elif self.tr.y <= other.bl.y:
            distance = round(math.fabs(other.bl.y - self.tr.y), 6)
        elif self.tr.x <= other.bl.x:
            distance = round(math.fabs(other.bl.x - self.tr.x), 6)
        elif self.bl.y >= other.tr.y:
            distance = round(math.fabs(other.tr.y - self.bl.y), 6)
        else:
            raise AssertionError

        return distance < space

    def is_in_curve(self):
        for point in [self.tl, self.tr, self.br, self.bl]:
            if not curve.is_point_in_curve(point):
                return False
        return True

    def clear_coords(self):
        self.shape = None
        self.tl = None
        self.tr = None
        self.br = None
        self.bl = None

    def get_indexes(self):
        """ Returns the indexes the given photo crosses in the plan. """

        keys = set()
        x_index_min = self.bl.get_x_index()
        x_index_max = self.tr.get_x_index()
        y_index_min = self.bl.get_y_index()
        y_index_max = self.tr.get_y_index()

        # Need to got from / to one more on the side to be sure we detect all photos
        for x in range(x_index_min - 1, x_index_max + 2):
            for y in range(y_index_min - 1, y_index_max + 2):
                keys.add((x, y))

        return sorted(keys)

    def on_the_left_of(self, other):
        return self.tr.x < other.bl.x

    def on_the_right_of(self, other):
        return self.bl.x > other.tr.x

    def on_the_top_of(self, other):
        return self.bl.y > other.tr.y

    def on_the_bottom_of(self, other):
        return self.tr.y < other.bl.y

    def __str__(self):
        return "Photo({}, {}, {}, {})".format(self.width, self.height, self.bl, self.name)

    def __repr__(self):
        return "P{}".format(self.name)
