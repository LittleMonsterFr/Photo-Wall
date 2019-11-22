from photo import Photo
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.patches import Rectangle
from point2D import Point2D
import curve
import progressBar
import matplotlib.ticker as plticker
import signal
from CoordinateGenerator import CoordinateGenerator
import math


def signal_handler(signum, frame):
    raise TimeoutError()


def set_photos_name(photo_list: [Photo]):
    for photo in photo_list:
        photo.name = photo_list.index(photo)


def get_photos_array(photos_dic) -> [Photo]:
    _photos = []
    for dic in photos_dic:
        for i in range(dic["num"]):
            _photos.append(Photo(dic["width"], dic["height"]))
    return _photos


def plot_photo(p: Photo):
    axs.add_patch(p.shape)
    plt.text(p.bl.x, p.bl.y, p.name, fontsize=8)
    plt.text(p.bl.x + p.width / 2, p.bl.y + p.height / 2, p.position,
             fontsize=8)


def place_photos_in_curve(photo_list, blp, trp):
    photo_space = 0.2
    coordinate_generator = CoordinateGenerator(blp.x, trp.x, bl.y, tr.y,
                                               0.2)
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

            """ At this point, the photo fits in the curve. """

            # Get the coordinates the photo crosses including the external edge
            photo_coordinate_indexes_external = photo.get_indexes(external=True)
            error = False

            for photo_coordinate_index in photo_coordinate_indexes_external:
                # Add an empty list for a given key if it isn't in the plan yet
                if photo_coordinate_index not in plan.keys():
                    plan[photo_coordinate_index] = []

                for neighbour in plan[photo_coordinate_index]:
                    if photo.overlap_with(neighbour):
                        error = True
                        break
                    if photo.too_close(neighbour, photo_space):
                        error = True
                        break
                    # Create a list of neighbours
                    photo.neighbours.add(neighbour)

                if error:
                    break

            if error:
                photo.clear_coords()
                photo.neighbours.clear()
                continue

            """
            At this point, the photo is not too close nor overlapping any
            of the photos around.
            """

            left = set()
            right = set()
            top = set()
            bottom = set()
            for neighbour in photo.neighbours:
                if neighbour.on_the_left_of(photo) and \
                        photo.horizontally_cross(neighbour):
                    left.add(neighbour)

                if neighbour.on_the_right_of(photo) and \
                        photo.horizontally_cross(neighbour):
                    right.add(neighbour)

                if neighbour.on_the_top_of(photo) and \
                        photo.vertically_cross(neighbour):
                    top.add(neighbour)

                if neighbour.on_the_bottom_of(photo) and \
                        photo.vertically_cross(neighbour):
                    bottom.add(neighbour)

            left = sorted(left, key=lambda photo_key: math.fabs(photo_key.tr.x - photo.bl.x))
            right = sorted(right, key=lambda photo_key: math.fabs(photo_key.bl.x - photo.tr.x))
            top = sorted(top, key=lambda photo_key: math.fabs(photo_key.bl.y - photo.tr.y))
            bottom = sorted(bottom, key=lambda photo_key: math.fabs(photo_key.tr.y - photo.bl.y))

            if len(left) > 0 and len(top) > 0:
                x_temp = left[0].br.x + photo_space
                y_temp = top[0].bl.y - photo_space - photo.height
                photo_fits = True
                photo.update_coordinates(Point2D(x_temp, y_temp))

                while photo_fits:
                    for neighbour in photo.neighbours:
                        if photo.overlap_with(neighbour) or photo.too_close(neighbour, photo_space):
                            photo_fits = False
                    break

                if photo_fits:
                    x_curr = x_temp
                    y_curr = y_temp
                else:
                    photo.update_coordinates(Point2D(x_curr, y_curr))

            for photo_coordinate_index in photo.get_indexes(external=False):
                plan[photo_coordinate_index].append(photo)

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
    plt.fill(xs, ys, "g", zorder=0)
    place_photos_in_curve(photos, bl, tr)
    # debug(photos, bl, tr)

    for p in photos:
        print(str(p))

    plt.show()
