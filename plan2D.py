from point2D import Point2D
from itertools import product
from photo import Photo


class Plan2D:

    def __init__(self, bl_point: Point2D, tr_point: Point2D, photo_space):
        self.__bl_point = bl_point
        self.__tr_point = tr_point
        self.__dict = {}
        self.__space = photo_space

    def add_photo(self, photo: Photo) -> bool:
        keys = photo.get_indexes()
        keys_to_add = []
        for key in keys:
            # Check if this is the first insert or not
            if len(self.__dict[key]) != 0:
                for p in self.__dict[key]:
                    if photo.overlap_with(p):
                        return False
                    if not photo.too_close(p, self.__space):
                        return False
            keys_to_add.append(key)

        # Reaching that line means the photo can be safely added to the plan
        for key in keys_to_add:
            self.__dict[key].append(photo)
        return True
