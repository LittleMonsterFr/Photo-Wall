from photo import Photo


class BitPacker:

    def __init__(self):
        self.bits_count = 0
        self.bytes = []
        self.value = 0

    def append(self, photo_list: [Photo]):
        for i in range(len(photo_list)):
            photo = photo_list[i]
            self.value = (self.value << 2) | (0b00000011 & photo.photo_format.value)
            self.bits_count += 2

            if self.bits_count == 8:
                self.bytes.append(self.value)
                self.value = 0
                self.bits_count = 0
