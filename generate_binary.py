from photo import Photo, PhotoFormat
from itertools import permutations
from bitpacker import BitPacker
import os
import math
from datetime import datetime, timedelta
import signal


def signal_handler(number, frame):
    global stop
    stop = True


def make_photo_list(double_photo_array: [[Photo]]) -> [Photo]:
    photo_list = [item for sublist in double_photo_array for item in sublist]
    for i in range(len(photo_list)):
        photo_list[i].index = i
    return photo_list


def photo_list_to_string(photo_list: [Photo]) -> str:
    res = ""
    letter_count = 0
    letter = photo_list[0].to_letter()
    for photo in photo_list:
        if photo.to_letter() != letter:
            res += "{}{}".format(letter_count, letter)
            letter = photo.to_letter()
            letter_count = 0

        letter_count += 1

    res += "{}{}".format(letter_count, letter)
    return res


def photo_list_from_string(list_string: str) -> [Photo]:
    num = ""
    res = []
    for char in list_string:
        if char.isdigit():
            num += char
        elif char.isalpha():
            count = int(num)
            for i in range(count):
                res.append(Photo.from_letter(char))
            num = ""
    return res


def verify_binary_size(set_length: int, photo_list_bit_length: int, binary_name: str) -> bool:
    stat_info = os.stat(binary_name)
    return math.ceil(set_length * photo_list_bit_length / 8) == stat_info.st_size


def generate_photo_permutations(photo_list: [Photo]):
    photo_list_iter = permutations(photo_list)
    res_set = set()
    for p_list in photo_list_iter:
        p_list_str = photo_list_to_string(p_list)
        res_set.add(p_list_str)

        if len(res_set) % 100 == 0:
            print("{} : {} items".format(datetime.now(), len(res_set)))

        if stop:
            break

    return res_set


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)
    stop = False

    start = datetime.now()

    FORMAT_15_10_PORTRAIT_COUNT = 24
    FORMAT_15_10_LANDSCAPE_COUNT = 2
    FORMAT_13_10_PORTRAIT_COUNT = 9
    FORMAT_13_10_LANDSCAPE_COUNT = 6

    # Add the photos in a list, each format being in a dictionary
    PHOTOS = [
        [Photo(PhotoFormat.FORMAT_15_10_PORTRAIT) for _ in range(FORMAT_15_10_PORTRAIT_COUNT)],
        [Photo(PhotoFormat.FORMAT_15_10_LANDSCAPE) for _ in range(FORMAT_15_10_LANDSCAPE_COUNT)],
        [Photo(PhotoFormat.FORMAT_13_10_PORTRAIT) for _ in range(FORMAT_13_10_PORTRAIT_COUNT)],
        [Photo(PhotoFormat.FORMAT_13_10_LANDSCAPE) for _ in range(FORMAT_13_10_LANDSCAPE_COUNT)],
    ]

    photos = make_photo_list(PHOTOS)
    photo_set = generate_photo_permutations(photos)

    file_name = "photo_set.bin"

    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file_name, "xb") as f:
        bit_packer = BitPacker(f)

        for format_str in photo_set:
            reconstructed_photo_list = photo_list_from_string(format_str)
            bit_packer.append(reconstructed_photo_list)

        bit_packer.finish()

    file_is_correct_size = verify_binary_size(len(photo_set), len(photos) * 2, file_name)

    end = datetime.now()

    elapsedTime = end - start

    print("\nGeneration done in {}".format(elapsedTime / timedelta(minutes=1)))

    print("File size is {}".format("correct" if file_is_correct_size else "incorrect"))

    exit(file_is_correct_size)
