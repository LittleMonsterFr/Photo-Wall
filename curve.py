import numpy as np
from scipy.integrate import quad
from point2D import Point2D
import math

# SIZE_COEFFICIENT = 0.445


def curve_x_function(t, curve_coefficient):
    return curve_coefficient * 16 * np.power(np.sin(t), 3)


def curve_x_prim_function(t, curve_coefficient):
    return curve_coefficient * 16 * 3 * np.power(np.sin(t), 2) * np.cos(t)


def curve_y_function(t, curve_coefficient):
    return curve_coefficient * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))


def curve_y_prim_function(t, curve_coefficient):
    return curve_coefficient * (-13 * np.sin(t) + 10 * np.sin(2 * t) + 6 * np.sin(3 * t) + 4 * np.sin(4 * t))


def winding_integrate_function(t, x0, y0, curve_coefficient):
    val1 = np.subtract(curve_x_function(t, curve_coefficient), x0)
    val2 = np.subtract(curve_y_function(t, curve_coefficient), y0)
    numerator_left = np.multiply(val1, curve_y_prim_function(t, curve_coefficient))
    numerator_right = np.multiply(val2, curve_x_prim_function(t, curve_coefficient))
    numerator = np.subtract(numerator_left, numerator_right)

    denominator = np.add(np.power(val1, 2), np.power(val2, 2))

    return np.inf if denominator == 0 else np.divide(numerator, denominator)


# https://math.stackexchange.com/questions/1308767/how-to-determine-whether-a-point-is-inside-a-closed-region-or-not
def is_point_in_curve_long(point: Point2D, curve_coefficient):
    res = quad(winding_integrate_function, 0, np.pi * 2, args=(point.x, point.y, curve_coefficient))
    if round(res[0], 10) == 0:
        return False
    return True


def curve_x_function_inverse(point, curve_coefficient):
    q = point.x / (16 * curve_coefficient)

    if q < 0:
        return -np.arcsin(np.power(-q, 1/3))
    elif q > 0:
        return np.arcsin(np.power(q, 1/3))
    else:
        return 0


def is_point_in_curve(point: Point2D, curve_coefficient):
    t = curve_x_function_inverse(point, curve_coefficient)

    y0 = curve_y_function(t, curve_coefficient)

    if t >= 0:
        y1 = curve_y_function(t - math.pi, curve_coefficient)
    else:
        y1 = curve_y_function(t + math.pi, curve_coefficient)

    return y0 >= point.y >= y1


def area_function(t, curve_coefficient):
    return curve_y_function(t, curve_coefficient) * curve_x_prim_function(t, curve_coefficient)


def curve_area(curve_coefficient):
    return quad(area_function, 0, 2 * np.pi, args=curve_coefficient)[0]
