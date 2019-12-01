from photo import Photo, PhotoFormat
from typing import BinaryIO
import sys
import math


class BitPacker:

    def __init__(self, file: BinaryIO):
        self.bits_count = 0
        self.bytes = []
        self.value = 0
        self.file = file

    def append(self, photo_list: [Photo]):
        for i in range(len(photo_list)):
            photo = photo_list[i]
            self.value = (self.value << 2) | (0b00000011 & photo.photo_format.value)
            self.bits_count += 2

            if self.bits_count == 8:
                b = self.value.to_bytes(1, byteorder=sys.byteorder)
                self.file.write(b)
                self.value = 0
                self.bits_count = 0

    def append_finish(self):
        b = self.value << (8 - self.bits_count)
        self.file.write(b.to_bytes(1, byteorder=sys.byteorder))

    def extract(self, photo_list_bit_size) -> [[Photo]]:
        res = []
        bytes_read = self.file.read()

        photo_list = []
        for byte in bytes_read:
            for i in range(0, 8, 2):
                value = ((byte << i) & 0b11000000) >> 6
                p = Photo(PhotoFormat(value))
                photo_list.append(p)
                self.bits_count += 2

                if self.bits_count == photo_list_bit_size:
                    res.append(photo_list)
                    photo_list = []
                    self.bits_count = 0

        return res
