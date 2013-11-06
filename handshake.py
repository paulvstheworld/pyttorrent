import struct

SIZE_PSTR_LEN = 1
SIZE_RESERVED_BYTES = 8
SIZE_INFO_HASH = 20
SIZE_PEER_ID = 20

class Handshake(object):
    def __init__(self, peer_id='',  
            pstr='BitTorrent protocol', 
            reserved='\x00\x00\x00\x00\x00\x00\x00\x00', 
            info_hash='', handshake_str=''):
        
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
