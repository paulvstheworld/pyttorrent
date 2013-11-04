import struct

PEER_ID = '-HS0001-123456789027'
PSTRLEN = '\x13'
PSTR = 'BitTorrent protocol'
RESERVED = '\x00\x00\x00\x00\x00\x00\x00\x00'

SIZE_PSTR_LEN = 1
SIZE_RESERVED_BYTES = 8
SIZE_INFO_HASH = 20
SIZE_PEER_ID = 20

class HandShake(object):
    def __init__(self, pstrlen='', pstr='', reserved='', peer_id='', info_hash=''):
        self.pstrlen = pstrlen
        self.pstr = pstr
        self.reserved = reserved
        self.peer_id = peer_id
        self.info_hash = info_hash
    
    
    def set_default_values(self, info_hash):
        self.pstrlen = len(PSTR)
        self.pstr = PSTR
        self.reserved = RESERVED
        self.peer_id = PEER_ID
        self.info_hash = info_hash
    
    
    def get_handshake_data_from_string(self, handshake_string):
        start_i = 0
        pstrlen = struct.unpack('B', handshake_string[start_i])[0]
        
        start_i += SIZE_PSTR_LEN
        pstr = handshake_string[start_i : pstrlen + start_i]
        
        start_i += pstrlen
        reserved = handshake_string[start_i : start_i + SIZE_RESERVED_BYTES]
        
        start_i += SIZE_RESERVED_BYTES
        info_hash = handshake_string[start_i : start_i + SIZE_INFO_HASH]
        
        start_i += SIZE_PEER_ID
        peer_id = handshake_string[start_i:]
        
        return pstrlen, pstr, reserved, info_hash, peer_id
        
        
    def set_handshake_data_from_string(self, handshake_string):
        pstrlen, pstr, reserved, info_hash, peer_id = self.get_handshake_data_from_string(handshake_string)
        self.pstrlen = pstrlen
        self.pstr = pstr
        self.reserved = reserved
        self.info_hash = info_hash
        self.peer_id = peer_id
    
    def __str__(self):
        return "%s%s%s%s%s" % (
            chr(self.pstrlen),
            self.pstr, 
            self.reserved, 
            self.info_hash, 
            self.peer_id)