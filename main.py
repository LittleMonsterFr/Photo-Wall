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
from CoordinateGenerator import CoordinateGenerator


def signal_handler(signum, frame):
    raise TimeoutError()


def set_photos_name(photo_list: [Photo]):
    for photo in photo_list:
        photo.name = photo_list.index(photo)


def get_photos_array(photos_dic) -> [Photo]:
    _photos = []
    for dic in photos_dic:
        for i in range(dic["num"]):
            p = Photo(dic["width"], dic["height"])
            _photos.append(p)
    return _photos


def plot_photo(p: Photo):
    axs.add_patch(p.shape)
    plt.text(p.bl.x, p.bl.y, p.name, fontsize=8)
    plt.text(p.bl.x + p.width / 2, p.bl.y + p.height / 2, p.position, fontsize=8)


def place_photos_in_curve(photo_list, blp, trp):
    photo_space = 0.2
    coordinate_generator = CoordinateGenerator(blp.x, trp.x, bl.y, tr.y, photo_space)
    updated_photo_list = list(photo_list)
    pos = 0
    coord = (bl.x, tr.y)

    plan = {}

    while coord is not None:

        progressBar.print_progress_bar(pos, len(photo_list), prefix='Progress:',
                                       suffix='Complete', length=100)

        # Set the current coordinates
        x_curr = coord[0]
        y_curr = coord[1]

        for photo in updated_photo_list:

            # Assign the corners of the photo
            photo.update_coordinates(Point2D(x_curr, y_curr))
            # Skip if all the corners are not in the curve
            if not photo.is_in_curve():
                # Clear the coordinates previously set to avoid corruption
                photo.clear_coords()
                continue

            # Get the coordinates the photo crosses
            keys = photo.get_indexes()

            # Temporary store the keys in this list
            keys_to_add = []
            error = False

            for key in keys:
                # Add an empty list for a given key if it isn't in the plan yet
                if key not in plan.keys():
                    plan[key] = []

                # Check if this is the first insert or not
                if len(plan[key]) != 0:
                    for already_added_photo in plan[key]:
                        if photo.overlap_with(already_added_photo):
                            error = True
                            break
                        if photo.too_close(already_added_photo, photo_space):
                            error = True
                            break

                    if error:
                        break

                keys_to_add.append(key)

            if error:
                photo.clear_coords()
                continue

            left = set()
            right = set()
            top = set()
            bottom = set()
            for key in keys_to_add:
                for already_added_photo in plan[key]:
                    if already_added_photo.on_the_left_of(photo):
                        left.add(already_added_photo)

                    if already_added_photo.on_the_right_of(photo):
                        right.add(already_added_photo)

                    if already_added_photo.on_the_top_of(photo):
                        top.add(already_added_photo)

                    if already_added_photo.on_the_bottom_of(photo):
                        bottom.add(already_added_photo)

            sorted(top, key=lambda photo_key: photo_key.bl.y < photo.tr.y)
            print(top)

            for key in keys_to_add:
                plan[key].append(photo)

            x_curr = photo.bl.x + photo.width
            photo.position = pos
            pos += 1
            plot_photo(photo)
            updated_photo_list.remove(photo)
            break

        if len(updated_photo_list) == 0:
            break

        coord = coordinate_generator.get_next_point(x_curr, y_curr)

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
    place_photos_in_curve(photos, bl, tr)
    # debug(photos, bl, tr)

    for p in photos:
        print(str(p))

    plt.show()
