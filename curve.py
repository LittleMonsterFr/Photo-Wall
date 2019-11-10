import numpy as np
from scipy.integrate import quad
from point2D import Point2D
import math

SIZE_COEFFICIENT = 0.5


def curve_x_function(t, size):
    return size * 16 * np.power(np.sin(t), 3)


def curve_x_prim_function(t, size):
    return size * 16 * 3 * np.power(np.sin(t), 2) * np.cos(t)


def curve_y_function(t, size):
    return size * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))


def curve_y_prim_function(t, size):
    return size * (-13 * np.sin(t) + 10 * np.sin(2 * t) + 6 * np.sin(3 * t) + 4 * np.sin(4 * t))


def winding_integrate_function(t, x0, y0, size):
    val1 = np.subtract(curve_x_function(t, size), x0)
    val2 = np.subtract(curve_y_function(t, size), y0)
    numerator_left = np.multiply(val1, curve_y_prim_function(t, size))
    numerator_right = np.multiply(val2, curve_x_prim_function(t, size))
    numerator = np.subtract(numerator_left, numerator_right)

    denominator = np.add(np.power(val1, 2), np.power(val2, 2))

    return np.inf if denominator == 0 else np.divide(numerator, denominator)


# https://math.stackexchange.com/questions/1308767/how-to-determine-whether-a-point-is-inside-a-closed-region-or-not
def is_point_in_curve(point: Point2D):
    res = quad(winding_integrate_function, 0, np.pi * 2, args=(point.x, point.y, SIZE_COEFFICIENT))
    if round(res[0], 10) == 0:
        return False
    return True


def is_point_in_curve_2(point: Point2D):
    size = SIZE_COEFFICIENT
    t = math.asin((point.x / (16 * size)) ** (1/3))

    y0 = curve_y_function(t, size)
    y1 = curve_y_function(t + math.pi, size)

    return y0 >= point.y >= y1
