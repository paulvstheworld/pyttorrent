import struct

SIZE_PSTR_LEN = 1
SIZE_RESERVED_BYTES = 8
SIZE_INFO_HASH = 20
SIZE_PEER_ID = 20
HANDSHAKE_WITHOUT_PROTOCOL_LEN = 49

class Handshake(object):
    def __init__(self, peer_id='',  
            pstr='BitTorrent protocol', 
            reserved='\x00\x00\x00\x00\x00\x00\x00\x00', 
            info_hash='', handshake_str=''):
        
        # TODO do more checking
        # check handshake size
        # check if certain kwargs were received
        if handshake_str:
            pstrlen, pstr, reserved, info_hash, peer_id = self.explode(handshake_str)
            
        self.peer_id = peer_id
        self.pstrlen = len(pstr)
        self.pstr = pstr
        self.reserved = reserved
        self.info_hash = info_hash


    def explode(self, handshake_str):
        start_i = 0
        pstrlen = struct.unpack('B', handshake_str[start_i])[0]
        
        start_i += SIZE_PSTR_LEN
        pstr = handshake_str[start_i : pstrlen + start_i]
        
        start_i += pstrlen
        reserved = handshake_str[start_i : start_i + SIZE_RESERVED_BYTES]
        
        start_i += SIZE_RESERVED_BYTES
        info_hash = handshake_str[start_i : start_i + SIZE_INFO_HASH]
        
        start_i += SIZE_PEER_ID
        peer_id = handshake_str[start_i:]
        
        return pstrlen, pstr, reserved, info_hash, peer_id


    def __str__(self):
        return "%s%s%s%s%s" % (chr(self.pstrlen), self.pstr, self.reserved, self.info_hash, self.peer_id,)


def parse_handshake(buffer):
    if buffer:
        pstr_len = struct.unpack('B', buffer[0])[0]
        handshake_size = pstr_len + HANDSHAKE_WITHOUT_PROTOCOL_LEN
        if handshake_size <= len(buffer):
            handshake = Handshake(handshake_str = buffer[0:handshake_size])
            return handshake, buffer[handshake_size:]
            
    return None, buffer