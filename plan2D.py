from point2D import Point2D
from itertools import product
import math


class Plan2D:

    def __init__(self, bl_point: Point2D, tr_point: Point2D):
        self.__bl_point = bl_point
        self.__tr_point = tr_point
        self.__dict = {}

        x_min = min(bl_point.get_x_index(), tr_point.get_x_index())
        x_max = max(bl_point.get_x_index(), tr_point.get_x_index())
        y_min = min(bl_point.get_y_index(), tr_point.get_y_index())
        y_max = max(bl_point.get_y_index(), tr_point.get_y_index())
        coordinates = list(product(range(x_min, x_max + 1),
                                   range(y_min, y_max + 1)))
        for coord in coordinates:
            dict[coord] =

