from bitpacker import BitPacker


def extract_binary():

    file_name = "photo_set.bin"

    res = None
    with open(file_name, "rb") as f:
        bit_packer = BitPacker(f)

        res = bit_packer.extract(41 * 2)

    return res
