import struct

PEER_ID = '-HS0001-123456789027'
PSTRLEN = '\x13'
PSTR = 'BitTorrent protocol'
RESERVED = '\x00\x00\x00\x00\x00\x00\x00\x00'

INDEX_HANDSHAKE_PSTRLEN = 0


def get_handshake(info_hash):
    # handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
    return "%s%s%s%s%s" % (PSTRLEN, PSTR, RESERVED, info_hash, PEER_ID)

def unpack_handshake(resp_handshake):
    # handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
    
    # first byte
    pstrlen = struct.unpack('B', resp_handshake[INDEX_HANDSHAKE_PSTRLEN])[0]
    
    # pstrlen number of bytes
    pstr = resp_handshake[1:pstrlen+1]
    
    # next 8 bytes
    reserved_bytes = resp_handshake[pstrlen+1: pstrlen+9]
    
    # next 20 bytes
    info_hash = resp_handshake[pstrlen+9:pstrlen+9+20]
    
    # last 20 bytes
    peer_id = resp_handshake[pstrlen+10+20:]
    
    return pstrlen, pstr, reserved_bytes, info_hash, peer_id