from matplotlib.patches import Rectangle
from point2D import Point2D


class Photo:

    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.__blp = None
        self.name = name
        self.shape = None
        self.__tl = None
        self.__tr = None
        self.__br = None
        self.__bl = None

    def get_corners(self):
        return [self.__tl, self.__tr, self.__br, self.__bl]

    @property
    def blp(self):
        return self.__blp

    @blp.setter
    def blp(self, value):
        self.__blp = value
        self.__tl = Point2D(self.blp.x, self.blp.y + self.height)
        self.__tr = Point2D(self.blp.x + self.width, self.blp.y + self.height)
        self.__br = Point2D(self.blp.x + self.width, self.blp.y)
        self.__bl = Point2D(self.blp.x, self.blp.y)
        self.shape = Rectangle((self.blp.x, self.blp.y), self.width, self.height, fill=False)

    def overlap_with(self, other):
        other_corners = other.get_corners()
        tr = other_corners[1]
        bl = other_corners[3]
        if tr.x < self.__bl.x or bl.y > self.__tr.y or bl.x > self.__tr.x or tr.y < self.__bl.y:
            return False

        return True

    def __str__(self):
        return "Photo({}, {}, {}, {})".format(self.width, self.height, self.blp, self.name)
