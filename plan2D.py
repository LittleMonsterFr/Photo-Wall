from point2D import Point2D
from itertools import product, combinations
from photo import Photo
import copy


class Plan2D:

    def __init__(self, bl_point: Point2D, tr_point: Point2D):
        self.__bl_point = bl_point
        self.__tr_point = tr_point
        self.__dict = {}
        self.__space = 0.2

        x_min = bl_point.get_x_index()
        x_max = tr_point.get_x_index()
        y_min = bl_point.get_y_index()
        y_max = tr_point.get_y_index()
        coordinates = list(product(range(x_min, x_max + 1),
                                   range(y_min, y_max + 1)))
        for coord in coordinates:
            self.__dict[coord] = []

    @staticmethod
    def __get_photo_indexes(photo: Photo):
        """ Returns the indexes the given photo crosses in the plan. """

        corners = photo.get_corners()
        couples = list(combinations(corners, 2))
        couples = [t for t in couples if t[0].get_x_index() == t[1].get_x_index()
                   or t[0].get_y_index() == t[1].get_y_index()]
        keys = set()
        for c in couples:
            x_indexes = c[0].get_x_indexes_between(c[1])
            y_indexes = c[0].get_y_indexes_between(c[1])

            if x_indexes is not None:
                for x_index in x_indexes:
                    keys.add((x_index, c[0].get_y_index()))
            else:
                for y_index in y_indexes:
                    keys.add((c[0].get_x_index(), y_index))
        return keys

    def add_photo(self, photo: Photo) -> bool:
        keys = self.__get_photo_indexes(photo)
        keys_to_add = []
        for key in keys:
            # Check if this is the first insert or not
            if len(self.__dict[key]) != 0:
                for p in self.__dict[key]:
                    if photo.overlap_with(p):
                        return False
                    # if photo.too_close_with(p, self.__space):
                    #     return False
                    # if photo.too_far_with(p, self.__space):
                    #     return False
                    # if not photo.at_good_distance_with(p, self.__space):
                    #     return False
            keys_to_add.append(key)

        # Reaching that line means the photo can be safely added to the plan
        for key in keys_to_add:
            self.__dict[key].append(photo)
        return True
