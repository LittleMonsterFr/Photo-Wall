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
import signal


def signal_handler(signum, frame):
    raise Exception()


def get_photos_array(photos_dic) -> [Photo]:
    _photos = []
    count = 0
    for dic in photos_dic:
        for i in range(dic["num"]):
            count += 1
            p = Photo(dic["width"], dic["height"], count)
            _photos.append(p)
    return _photos


def is_photo_in_curve(p: Photo):
    for point in p.get_corners():
        if not curve.is_point_in_curve(point):
            return False
    return True


def plot_photo(p: Photo):
    axs.add_patch(p.shape)
    plt.text(p.bl.x, p.bl.y, p.name, fontsize=10)


def random_place_photos_in_heart(photo_list, blp, trp):
    plan = Plan2D(blp, trp)

    signal.alarm(60)
    count = 0
    while count < len(photo_list):
        x_rand = random.uniform(blp.x, trp.x)
        y_rand = random.uniform(blp.y, trp.y)
        photo = photo_list[count]
        photo.bl = Point2D(x_rand, y_rand)
        if is_photo_in_curve(photo):
            if plan.add_photo(photo):
                photo.name = str(count)
                plot_photo(photo)
                count += 1
                progressBar.print_progress_bar(count, len(photos), prefix='Progress:', suffix='Complete', length=50)


if __name__ == "__main__":
    # Seed the random number generator to have the same results over each iteration
    random.seed(42)

    signal.signal(signal.SIGALRM, signal_handler)

    # Define the number of photos for each format (width / height (cm))
    FORMAT_15_10_PORTRAIT = 24
    FORMAT_15_10_LANDSCAPE = 2
    FORMAT_13_10_PORTRAIT = 9
    FORMAT_13_10_LANDSCAPE = 6

    # Add the photos in a list, each format being in a dictionary
    PHOTOS = [
        # The width and height of the photos are reduced to the values of the ratio
        {"num": FORMAT_15_10_PORTRAIT, "width": 1, "height": 1.5},
        {"num": FORMAT_15_10_LANDSCAPE, "width": 1.5, "height": 1},
        {"num": FORMAT_13_10_PORTRAIT, "width": 1, "height": 1.3},
        {"num": FORMAT_13_10_LANDSCAPE, "width": 1.3, "height": 1},
    ]

    # Get the axes of the plot
    fig, axs = plt.subplots()
    axs.grid(True, which='both')
    axs.axis('equal')
    loc = plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    axs.xaxis.set_major_locator(loc)
    axs.yaxis.set_major_locator(loc)

    photos = get_photos_array(PHOTOS)
    random.shuffle(photos)

    ts = np.linspace(0, 2 * np.pi, num=100)
    xs = curve.curve_x_function(ts, curve.SIZE_COEFFICIENT)
    ys = curve.curve_y_function(ts, curve.SIZE_COEFFICIENT)
    bl = Point2D(min(xs), min(ys))
    tr = Point2D(max(xs), max(ys))

    progressBar.print_progress_bar(0, len(photos), prefix='Progress:', suffix='Complete', length=50)

    external_heart = Rectangle((bl.x, bl.y), abs(tr.x - bl.x), abs(tr.y - bl.y), fill=False)
    axs.add_patch(external_heart)
    plt.fill(xs, ys, zorder=0)
    try:
        random_place_photos_in_heart(photos, bl, tr)
    except Exception:
        pass
    plt.show()