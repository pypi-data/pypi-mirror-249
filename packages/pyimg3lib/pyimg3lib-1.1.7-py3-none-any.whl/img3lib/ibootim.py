
from .utils import getBufferAtIndex, formatData

import lzss


def parseiBootIM(data):
    head_size = 24

    head_data = getBufferAtIndex(data, 0, head_size)

    (
        signature,
        idk,
        compression_type,
        data_format,
        width,
        height
    ) = formatData('<8sI4s4s2H', head_data, False)

    padding_len = 0x28

    # padding = getBufferAtIndex(data, head_size, padding_len)

    idk = idk.to_bytes(4, 'little')

    compression_type = compression_type[::-1]

    data_format = data_format[::-1]

    start = head_size + padding_len

    ibootim_data_len = len(data) - start

    ibootim_data = getBufferAtIndex(data, start, ibootim_data_len)

    ibootim_data_decompressed = lzss.decompress(ibootim_data)

    with open('test.bin', 'wb') as f:
        f.write(ibootim_data_decompressed)

    pass
