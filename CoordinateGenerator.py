
class CoordinateGenerator:

    def __init__(self, x_min, x_max, y_min, y_max, step):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.step = step

    def get_next_point(self, x_curr: float, y_curr: float) -> (float, float):
        x_next = x_curr + self.step
        y_next = y_curr

        if x_next > self.x_max:
            x_next = self.x_min
            y_next -= self.step

            if y_next < self.y_min:
                return None

        return x_next, y_next
