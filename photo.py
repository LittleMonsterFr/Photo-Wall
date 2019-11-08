from matplotlib.patches import Rectangle
from point2D import Point2D


class Photo:

    def __init__(self, width, height, x, y, name):
        self.width = width
        self.height = height
        self.blp = Point2D(x, y)
        self.name = name
        self.shape = Rectangle((x, y), width, height, fill=False)
        self.tl = Point2D(self.blp.x, self.blp.y + self.height)
        self.tr = Point2D(self.blp.x + self.width, self.blp.y + self.height)
        self.br = Point2D(self.blp.x + self.width, self.blp.y)
        self.bl = Point2D(self.blp.x, self.blp.y)

    def get_corners(self):
        return [self.tl, self.tr, self.br, self.bl]

    def __str__(self):
        return "Photo({}, {}, {}, {})".format(self.width, self.height, self.blp, self.name)
