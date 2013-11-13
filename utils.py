import math
import struct

def get_4_bytes_in_decimal(bytes):
    dec_value = 0
    dec_value += struct.unpack('B', bytes[0])[0] * int(math.pow(256, 3))
    dec_value += struct.unpack('B', bytes[1])[0] * int(math.pow(256, 2))
    dec_value += struct.unpack('B', bytes[2])[0] * int(math.pow(256, 1))
    dec_value += struct.unpack('B', bytes[3])[0]

    return dec_value