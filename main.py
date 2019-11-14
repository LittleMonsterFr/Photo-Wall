from photo import Photo
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.patches import Rectangle
from point2D import Point2D
from plan2D import Plan2D
import curve
import progressBar
import matplotlib.ticker as plticker
from itertools import product
import signal


def signal_handler(signum, frame):
    raise TimeoutError()


def set_photos_name(photo_list: [Photo]):
    for photo in photo_list:
        photo.name = photo_list.index(photo)


def generate_points_to_try(blp, trp, step):
    x_range = np.arange(blp.x, trp.x, step)
    y_range = np.arange(blp.y, trp.y, step)
    return sorted([Point2D(elt[0], elt[1]) for elt in list(product(x_range,
                                                                   y_range))])


def get_photos_array(photos_dic) -> [Photo]:
    _photos = []
    count = 0
    for dic in photos_dic:
        for i in range(dic["num"]):
            count += 1
            p = Photo(dic["width"], dic["height"])
            _photos.append(p)
    return _photos


def is_photo_in_curve(p: Photo):
    for point in p.get_corners():
        if not curve.is_point_in_curve(point):
            return False
    return True


def plot_photo(p: Photo):
    axs.add_patch(p.shape)
    plt.text(p.bl.x, p.bl.y, p.name, fontsize=8)
    plt.text(p.bl.x + p.width / 2, p.bl.y + p.height / 2, p.position, fontsize=8)


def debug(photo_list, blp, trp):
    point = Point2D(0, 0)
    plan = Plan2D(blp, trp)

    photo1 = photo_list[0]
    photo1.bl = point
    if photo1.is_in_curve():
        if plan.add_photo(photo1):
            plot_photo(photo1)

    point = Point2D(1.2, 0)
    photo2 = photo_list[1]
    photo2.bl = point
    if photo2.is_in_curve():
        if plan.add_photo(photo2):
            plot_photo(photo2)


def random_place_photos_in_heart(photo_list, blp, trp):
    plan = Plan2D(blp, trp)

    points_to_try = generate_points_to_try(blp, trp, 0.1)

    updated_photo_list = list(photo_list)
    pos = 0
    for point in points_to_try:

        progressBar.print_progress_bar(points_to_try.index(point),
                                       len(points_to_try), prefix='Progress:',
                                       suffix='Complete', length=100)

        for photo in updated_photo_list:

            # Assign the corners of the photo
            photo.bl = point
            # Skip if all the corners are not in the curve
            if not photo.is_in_curve():
                # Clear the coordinates previously set to avoid corruption
                photo.clear_coords()
                continue

            if plan.add_photo(photo):
                photo.position = pos
                pos += 1
                plot_photo(photo)
                updated_photo_list.remove(photo)
                break
            else:
                photo.clear_coords()

    print("\n{} photos left : {}".format(len(updated_photo_list),
                                       updated_photo_list))


if __name__ == "__main__":
    # Seed the random number generator to have the same results over each
    # iteration
    random.seed(42)

    signal.signal(signal.SIGALRM, signal_handler)

    # Define the number of photos for each format (width / height (cm))
    FORMAT_15_10_PORTRAIT = 24
    FORMAT_15_10_LANDSCAPE = 2
    FORMAT_13_10_PORTRAIT = 9
    FORMAT_13_10_LANDSCAPE = 6

    # Add the photos in a list, each format being in a dictionary
    PHOTOS = [
        # The width and height of the photos are reduced to the values of the
        # ratio
        {"num": FORMAT_15_10_PORTRAIT, "width": 1, "height": 1.5},
        {"num": FORMAT_15_10_LANDSCAPE, "width": 1.5, "height": 1},
        {"num": FORMAT_13_10_PORTRAIT, "width": 1, "height": 1.3},
        {"num": FORMAT_13_10_LANDSCAPE, "width": 1.3, "height": 1},
    ]

    # Get the axes of the plot
    fig, axs = plt.subplots()
    axs.grid(True, which='both')
    axs.axis('equal')
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=1.0)
    axs.xaxis.set_major_locator(loc)
    axs.yaxis.set_major_locator(loc)

    photos = get_photos_array(PHOTOS)
    random.shuffle(photos)
    set_photos_name(photos)

    ts = np.linspace(-np.pi, np.pi, num=100)
    xs = curve.curve_x_function(ts, curve.SIZE_COEFFICIENT)
    ys = curve.curve_y_function(ts, curve.SIZE_COEFFICIENT)
    bl = Point2D(min(xs), min(ys))
    tr = Point2D(max(xs), max(ys))

    progressBar.print_progress_bar(0, len(photos), prefix='Progress:',
                                   suffix='Complete', length=100)

    external_heart = Rectangle((bl.x, bl.y), abs(tr.x - bl.x), abs(tr.y - bl.y),
                               fill=False)
    axs.add_patch(external_heart)
    plt.fill(xs, ys, zorder=0)
    # curve.is_point_in_curve_2(Point2D(-3, -1))
    random_place_photos_in_heart(photos, bl, tr)
    # debug(photos, bl, tr)

    for photo in photos:
        print(str(photo))
    plt.show()
