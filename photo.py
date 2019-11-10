from matplotlib.patches import Rectangle
from point2D import Point2D


class Photo:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.name = None
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
        tr = other_corners[1]
        bl = other_corners[3]
        if tr.x < self.__bl.x or bl.y > self.__tr.y or bl.x > self.__tr.x or tr.y < self.__bl.y:
            return False

        return True

    def too_close_with(self, other, space):
        other_corners = other.get_corners()
        tr = other_corners[1]
        bl = other_corners[3]
        if abs(tr.x - self.__bl.x) < space or abs(bl.y - self.__tr.y) < space or abs(bl.x - self.__tr.x) < space \
                or abs(tr.y - self.__bl.y) < space:
            return True

        return False

    def too_far_with(self, other, space):
        other_corners = other.get_corners()
        tr = other_corners[1]
        bl = other_corners[3]
        if abs(tr.x - self.__bl.x) > space or abs(bl.y - self.__tr.y) > space or abs(bl.x - self.__tr.x) > space \
                or abs(tr.y - self.__bl.y) > space:
            return True

        return False

    def at_good_distance_with(self, other, space):
        other_corners = other.get_corners()
        tr = other_corners[1]
        bl = other_corners[3]
        if abs(tr.x - self.__bl.x) == space or abs(bl.y - self.__tr.y) == space or abs(bl.x - self.__tr.x) == space \
                or abs(tr.y - self.__bl.y) == space:
            return True

        return False

    def __str__(self):
        return "Photo({}, {}, {}, {})".format(self.width, self.height, self.bl, self.name)

    def __repr__(self):
        return "P{}".format(self.name)
