
class Photo:

    def __init__(self, width, height, x, y, name):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return "P(" + str(self.width) + ", " + str(self.height) + ", " + str(self.x) + \
               ", " + str(self.y) + ", " + str(self.name) + ")"
