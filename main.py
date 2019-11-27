from photo import Photo, PhotoFormat
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.patches import Rectangle
from point2D import Point2D
import curve
import progressBar
import matplotlib.ticker as plticker
import signal
from CoordinateGenerator import CoordinateGenerator, Side
import math
import sys
import itertools
import pickle
from bitpacker import BitPacker


def signal_handler(signum, frame):
    print()
    sys.exit(0)


def make_photo_list(pre_photos_list: [[Photo]]):
    _photo_list = [item for sublist in pre_photos_list for item in sublist]
    for i in range(len(_photo_list)):
        _photo_list[i].index = i
    return _photo_list


def photo_list_to_string(photo_list: [Photo]) -> str:
    res = ""
    letter_count = 0
    letter = photo_list[0].format_letter
    for photo in photo_list:
        if photo.format_letter != letter:
            res += "{}{}".format(letter_count, letter)
            letter = photo.format_letter
            letter_count = 0

        letter_count += 1

    res += "{}{}".format(letter_count, letter)
    return res


def generate_photo_permutations(photo_list: [Photo]):
    photo_list_iter = itertools.permutations(photo_list)
    photo_set = set()
    for p_list in photo_list_iter:
        p_list_str = photo_list_to_string(p_list)
        photo_set.add(p_list_str)

        if len(photo_set) % 100 == 0:
            print("photo set len is {}".format(len(photo_set)))


def plot_photo(p: Photo):
    axs.add_patch(p.shape)
    plt.text(p.bl.x, p.bl.y, p.index, fontsize=8)
    plt.text(p.bl.x + p.width / 2, p.bl.y + p.height / 2, p.position,
             fontsize=8)
    fig.canvas.draw()


def place_photos_in_curve(photo_list, blp, trp, photo_space, point_unit, curve_coefficient):
    coordinate_generator = CoordinateGenerator(blp.x, trp.x, bl.y, tr.y, point_unit)
    updated_photo_list = list(photo_list)
    pos = 0
    coord = coordinate_generator.get_start()

    plan = {}

    while coord is not None:

        progressBar.print_progress_bar(pos, len(photo_list), prefix='Progress:',
                                       suffix='Complete', length=100)

        # Set the current coordinates
        x_curr = coord[0]
        y_curr = coord[1]

        if curve.is_point_in_curve(Point2D(x_curr, y_curr), curve_coefficient):

            for photo in updated_photo_list:

                # Assign the corners of the photo
                photo.set_center(Point2D(x_curr, y_curr))
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
                for neighbour in photo.neighbours:
                    if neighbour.on_the_left_of(photo) and \
                            photo.has_close_left_neighbour(neighbour, photo_space):
                        left.add(neighbour)

                    if neighbour.on_the_right_of(photo) and \
                            photo.has_close_right_neighbour(neighbour, photo_space):
                        right.add(neighbour)

                    if neighbour.on_the_top_of(photo) and \
                            photo.has_close_top_neighbour(neighbour, photo_space):
                        top.add(neighbour)

                left = sorted(left, key=lambda photo_key: math.fabs(photo_key.br.x - photo.bl.x))
                right = sorted(right, key=lambda photo_key: math.fabs(photo_key.bl.x - photo.br.x))
                top = sorted(top, key=lambda photo_key: math.fabs(photo_key.bl.y - photo.tl.y))

                side = coordinate_generator.get_curve_side(x_curr)
                if ((side == Side.LEFT and len(right) > 0) or
                    (side == Side.RIGHT and len(left) > 0) or
                   side == Side.MIDDLE):

                    if side == Side.LEFT:
                        x_temp = right[0].bl.x - photo_space - photo.width / 2
                    elif side == Side.RIGHT:
                        x_temp = left[0].br.x + photo_space + photo.width / 2
                    else:
                        x_temp = x_curr

                    if len(top) > 0:
                        y_temp = top[0].bl.y - photo_space - photo.height / 2
                    else:
                        y_temp = y_curr
                    photo.set_center(Point2D(x_temp, y_temp))
                    photo_fits = True

                    if not photo.is_in_curve():
                        photo_fits = False

                    while photo_fits:
                        for neighbour in photo.neighbours:
                            if photo.overlap_with(neighbour) or photo.too_close(neighbour, photo_space):
                                photo_fits = False
                        break

                    if photo_fits:
                        x_curr = x_temp
                        y_curr = y_temp
                    else:
                        photo.set_center(Point2D(x_curr, y_curr))

                for photo_coordinate_index in photo.get_indexes(external=False):
                    plan[photo_coordinate_index].append(photo)

                x_curr, y_curr = coordinate_generator.get_next_point_after_photo(x_curr, y_curr, photo)
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

    signal.signal(signal.SIGINT, signal_handler)

    # Define the number of photos for each format (width / height (cm))
    FORMAT_15_10_PORTRAIT_COUNT = 24
    FORMAT_15_10_LANDSCAPE_COUNT = 2
    FORMAT_13_10_PORTRAIT_COUNT = 9
    FORMAT_13_10_LANDSCAPE_COUNT = 6

    CURVE_COEFFICIENT = 0.445
    PHOTO_SPACE = 0.1
    POINT_UNIT = 0.5

    # Add the photos in a list, each format being in a dictionary
    PHOTOS = [
        [Photo(1, 1.5, PhotoFormat.FORMAT_13_10_PORTRAIT, CURVE_COEFFICIENT) for _ in range(FORMAT_15_10_PORTRAIT_COUNT)],
        [Photo(1.5, 1, PhotoFormat.FORMAT_15_10_LANDSCAPE, CURVE_COEFFICIENT) for _ in range(FORMAT_15_10_LANDSCAPE_COUNT)],
        [Photo(1, 1.3, PhotoFormat.FORMAT_13_10_PORTRAIT, CURVE_COEFFICIENT) for _ in range(FORMAT_13_10_PORTRAIT_COUNT)],
        [Photo(1.3, 1, PhotoFormat.FORMAT_13_10_LANDSCAPE, CURVE_COEFFICIENT) for _ in range(FORMAT_13_10_LANDSCAPE_COUNT)],
    ]

    PHOTOS = make_photo_list(PHOTOS)

    bit_packer = BitPacker()
    # bits = bit_packer.append(PHOTOS)
    # photo_list_str = photo_list_to_string(PHOTOS)

    generate_photo_permutations(PHOTOS)

    exit(0)

    # Get the axes of the plot
    fig, axs = plt.subplots()
    fig.canvas.manager.full_screen_toggle()

    # axs.grid(True, which='both')
    axs.axis('equal')

    # this locator puts ticks at regular intervals
    # loc = plticker.MultipleLocator(base=1.0)
    # axs.xaxis.set_major_locator(loc)
    # axs.yaxis.set_major_locator(loc)

    # random.shuffle(photos)
    # set_photos_name(photos)

    ts = np.linspace(-np.pi, np.pi, num=100)
    xs = curve.curve_x_function(ts, CURVE_COEFFICIENT)
    ys = curve.curve_y_function(ts, CURVE_COEFFICIENT)
    bl = Point2D(min(xs), min(ys))
    tr = Point2D(max(xs), max(ys))

    # progressBar.print_progress_bar(0, len(photos), prefix='Progress:',
    #                                suffix='Complete', length=100)

    # external_heart = Rectangle((bl.x, bl.y), abs(tr.x - bl.x), abs(tr.y - bl.y),
    #                            fill=False)
    # axs.add_patch(external_heart)
    plt.fill(xs, ys, "g", zorder=0)
    plt.axis('off')

    plt.show(block=False)

    # place_photos_in_curve(photos, bl, tr, PHOTO_SPACE, POINT_UNIT, CURVE_COEFFICIENT)
    axs.text(0, 0, "Some text", transform=axs.transAxes, fontsize=12)

    curve_area = curve.curve_area(CURVE_COEFFICIENT)
    print("Curve area : {}".format(curve_area))

    area_sum = 0
    # for p in photos:
    #     area_sum += p.width * p.height
        # print(str(p))

    print("Photos area : {}".format(area_sum))
    print("Coverage : {:2f} %".format(area_sum * 100 / curve_area))
    plt.show()
