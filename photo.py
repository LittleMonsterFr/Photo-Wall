from matplotlib.patches import Rectangle
from point2D import Point2D
import curve
import math


class Photo:

    def __init__(self, width, height, curve_coefficient):
        self.index = None
        self.width = width
        self.height = height
        self.curve_coefficient = curve_coefficient
        self.position = None
        self.shape = None
        self.tl = None
        self.tr = None
        self.br = None
        self.bl = None
        self.__center = None
        self.neighbours = set()

    def set_center(self, center_point: Point2D):
        self.__center = center_point
        half_width = self.width / 2
        half_height = self.height / 2
        self.bl = Point2D(center_point.x - half_width, center_point.y - half_height)
        self.tl = Point2D(center_point.x - half_width, center_point.y + half_height)
        self.tr = Point2D(center_point.x + half_width, center_point.y + half_height)
        self.br = Point2D(center_point.x + half_width, center_point.y - half_height)
        self.shape = Rectangle((self.bl.x, self.bl.y), self.width, self.height, fill=False)

    def overlap_with(self, other):
        if other.on_the_left_of(self) or \
                other.on_the_top_of(self) or \
                other.on_the_right_of(self) or \
                other.on_the_bottom_of(self):
            return False

        return True

    def too_close(self, other, space):
        res = False

        #  Left
        if other.on_the_left_of(self):
            if other.br.y >= self.tl.y + space or other.tr.y <= self.bl.y - space:
                res |= False
            else:
                res |= round(math.fabs(other.tr.x - self.bl.x), 2) < space

        # Top
        if other.on_the_top_of(self):
            if other.br.x <= self.tl.x - space or other.bl.x >= self.tr.x + space:
                res |= False
            else:
                res |= round(math.fabs(other.bl.y - self.tr.y), 2) < space

        # Right
        if other.on_the_right_of(self):
            if other.bl.y >= self.tr.y + space or other.tl.y <= self.br.y - space:
                res |= False
            else:
                res |= round(math.fabs(other.bl.x - self.tr.x), 2) < space

        # Bottom
        if other.on_the_bottom_of(other):
            if other.tr.x <= self.bl.x - space or other.tl.x >= self.br.x + space:
                res |= False
            else:
                res |= round(math.fabs(other.tr.y - self.bl.y), 2) < space

        return res

    def is_in_curve(self):
        for point in [self.tl, self.tr, self.br, self.bl, self.__center]:
            if not curve.is_point_in_curve(point, self.curve_coefficient):
                return False

        y0 = curve.curve_y_function(0, self.curve_coefficient)

        if self.tl.y >= y0 and (self.tl.x * self.tr.x) < 0:
            return False

        return True

    def clear_coords(self):
        self.shape = None
        self.tl = None
        self.tr = None
        self.br = None
        self.bl = None
        self.__center = None

    def get_indexes(self, external=False):
        """ Returns the indexes the given photo crosses in the plan. """

        keys = set()
        x_index_min = self.bl.get_x_index() + (-1 if external else 0)
        x_index_max = self.tr.get_x_index() + (2 if external else 1)
        y_index_min = self.bl.get_y_index() + (-1 if external else 0)
        y_index_max = self.tr.get_y_index() + (2 if external else 1)

        for x in range(x_index_min, x_index_max):
            for y in range(y_index_min, y_index_max):
                keys.add((x, y))

        return sorted(keys)

    def on_the_left_of(self, other):
        return self.tr.x <= other.bl.x

    def on_the_right_of(self, other):
        return self.bl.x >= other.tr.x

    def on_the_top_of(self, other):
        return self.bl.y >= other.tr.y

    def on_the_bottom_of(self, other):
        return self.tr.y <= other.bl.y

    def has_close_left_neighbour(self, other, space):
        return (other.tr.y >= self.tl.y + space and self.bl.y - space >= other.br.y) or \
               (other.tr.y <= self.tl.y + space and self.bl.y - space <= other.br.y) or \
               other.br.y <= self.tl.y + space <= other.tr.y or \
               other.br.y <= self.bl.y - space <= other.tr.y

    def has_close_right_neighbour(self, other, space):
        return (other.tl.y >= self.tr.y + space and self.br.y - space >= other.bl.y) or \
               (other.tl.y <= self.tr.y + space and self.br.y - space <= other.bl.y) or \
               other.bl.y <= self.tr.y + space <= other.tl.y or \
               other.bl.y <= self.br.y - space <= other.tl.y

    def has_close_top_neighbour(self, other, space):
        return (other.br.x >= self.tr.x + space and self.tl.x - space >= other.bl.x) or \
               (other.br.x <= self.tr.x + space and self.tl.x - space <= other.bl.x) or \
               other.bl.x <= self.tr.x + space <= other.br.x or \
               other.bl.x <= self.tl.x - space <= other.br.x

    def vertically_cross(self, other):
        return other.bl.x <= self.bl.x <= other.br.x or \
               other.bl.x <= self.br.x <= other.br.x or \
               (self.bl.x <= other.bl.x and other.br.x <= self.br.x)

    def horizontally_cross(self, other):
        return other.bl.y <= self.bl.y <= other.tl.y or \
               other.bl.y <= self.tl.y <= other.tl.y or \
               (self.bl.y <= other.bl.y and other.tl.y <= self.tl.y)

    def __str__(self):
        return "Photo({}, {}, {}, {})".format(self.width, self.height, self.__center, self.name)

    def __repr__(self):
        return "P{}".format(self.index)

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height

    def __ne__(self, other):
        return self.width != other.width or self.height != other.height

    def __hash__(self):
        return hash((self.width, self.height, self.index))
