from photo import Photo
import matplotlib.pyplot as plt
import matplotlib.axes
import numpy as np
import random
from scipy.integrate import quad

SIZE_COEFFICIENT = 0.5


def get_photos_array(photos_dic) -> [Photo]:
    _photos = []
    count = 0
    for dic in photos_dic:
        for i in range(dic["num"]):
            count += 1
            p = Photo(dic["width"], dic["height"], 0, 0, count)
            _photos.append(p)
    return _photos


# https://math.stackexchange.com/questions/1308767/how-to-determine-whether-a-point-is-inside-a-closed-region-or-not
def winding_integrate_function(t, x0, y0):
    val1 = np.subtract(heart_x_function(t), x0)
    val2 = np.subtract(heart_y_function(t), y0)
    numerator_left = np.multiply(val1, heart_y_prim_function(t))
    numerator_right = np.multiply(val2, heart_x_prim_function(t))
    numerator = np.subtract(numerator_left, numerator_right)

    denominator = np.add(np.power(val1, 2), np.power(val2, 2))

    return np.inf if denominator == 0 else np.divide(numerator, denominator)


def is_photo_in_heart(p: Photo):
    for point in p.get_corners():
        res = quad(winding_integrate_function, 0, np.pi * 2, args=(point.x, point.y))
        if round(res[0], 10) == 0:
            return False
    return True


def heart_x_function(t):
    return SIZE_COEFFICIENT * 16 * np.power(np.sin(t), 3)


def heart_x_prim_function(t):
    return SIZE_COEFFICIENT * 16 * 3 * np.power(np.sin(t), 2) * np.cos(t)


def heart_y_function(t):
    return SIZE_COEFFICIENT * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))


def heart_y_prim_function(t):
    return SIZE_COEFFICIENT * (-13 * np.sin(t) + 10 * np.sin(2 * t) + 6 * np.sin(3 * t) + 4 * np.sin(4 * t))


def add_photo_to_plot(ax: matplotlib.axes.Axes, p: Photo):
    ax.add_patch(p.shape)


if __name__ == "__main__":
    random.seed(42)

    FORMAT_15_10_PORTRAIT = 24
    FORMAT_15_10_LANDSCAPE = 2
    FORMAT_13_10_PORTRAIT = 9
    FORMAT_13_10_LANDSCAPE = 6

    PHOTOS = [
        {"num": FORMAT_15_10_PORTRAIT, "width": 1, "height": 1.5},
        {"num": FORMAT_15_10_LANDSCAPE, "width": 1.5, "height": 1},
        {"num": FORMAT_13_10_PORTRAIT, "width": 1, "height": 1.3},
        {"num": FORMAT_13_10_LANDSCAPE, "width": 1.3, "height": 1},
    ]

    axs = plt.gca()
    # axs.grid(True, which='both')
    axs.axis('equal')

    photos = get_photos_array(PHOTOS)
    random.shuffle(photos)

    photo = Photo(1, 1.5, 7, 2, 0)
    print(photo)
    add_photo_to_plot(axs, photo)
    print(is_photo_in_heart(photo))

    ts = np.linspace(0, 2 * np.pi, num=100)
    plt.fill(heart_x_function(ts), heart_y_function(ts), zorder=0)
    plt.show()
