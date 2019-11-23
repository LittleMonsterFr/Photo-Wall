import photo
from enum import Enum


class Side(Enum):
    LEFT = 0,
    RIGHT = 1,
    MIDDLE = 2,


class CoordinateGenerator:

    def __init__(self, x_min, x_max, y_min, y_max, step):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.step = step
        self.x_mid = (x_min + x_max) / 2

    def get_next_point(self, x_curr: float, y_curr: float) -> (float, float):
        if x_curr >= self.x_mid:
            x_next = x_curr + self.step
        else:
            x_next = x_curr - self.step

        y_next = y_curr

        if x_next > self.x_max or x_next < self.x_min:
            if x_next > self.x_max:
                x_next = self.x_mid - self.step
            else:
                x_next = self.x_mid
                y_next -= self.step

                if y_next < self.y_min:
                    return None

        return x_next, y_next

    def get_next_point_after_photo(self, x_curr: float, y_curr: float, p: photo.Photo):
        if x_curr >= self.x_mid:
            x = x_curr + p.width / 2
        else:
            x = x_curr - p.width / 2

        return self.get_next_point(x, y_curr)

    def get_start(self):
        return self.x_mid, self.y_max

    def get_curve_side(self, x_curr) -> Side:
        if x_curr > self.x_mid:
            return Side.RIGHT
        elif x_curr < self.x_mid:
            return Side.LEFT
        else:
            return Side.MIDDLE
