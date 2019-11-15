from point2D import Point2D
from itertools import product
from photo import Photo


class Plan2D:

    def __init__(self, bl_point: Point2D, tr_point: Point2D, photo_space):
        self.__bl_point = bl_point
        self.__tr_point = tr_point
        self.__dict = {}
        self.__space = photo_space

        x_min = bl_point.get_x_index()
        x_max = tr_point.get_x_index()
        y_min = bl_point.get_y_index()
        y_max = tr_point.get_y_index()
        coordinates = list(product(range(x_min, x_max + 1),
                                   range(y_min, y_max + 1)))
        for coord in coordinates:
            self.__dict[coord] = []

    def add_photo(self, photo: Photo) -> bool:
        keys = photo.get_indexes()
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
                    if not photo.close_enough(p, self.__space):
                        return False
            keys_to_add.append(key)

        # Reaching that line means the photo can be safely added to the plan
        for key in keys_to_add:
            self.__dict[key].append(photo)
        return True
