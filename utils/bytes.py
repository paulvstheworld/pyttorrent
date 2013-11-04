import math
import struct

class Not4Bytes(Exception):
    def __init__(self, message, Errors):
        Exception.__init__(self, message)
        self.Errors = Errors

def get_4_bytes_decimal_value(bytes):
    value = 0
    
    if len(bytes) != 4:
        raise Not4Bytes('bytes must 4 bytes long')
    
    value += struct.unpack('B', bytes[0])[0] * int(math.pow(256, 3))
    value += struct.unpack('B', bytes[1])[0] * int(math.pow(256, 2))
    value += struct.unpack('B', bytes[2])[0] * int(math.pow(256, 1))
    value += struct.unpack('B', bytes[3])[0]
    
    return value
    
