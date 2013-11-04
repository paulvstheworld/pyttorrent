PEER_STATE_DISCONNECTED = DISCONNECTED

class Peer(object):
    def __init__(self, ip, port, peer_id):
        self._ip = ip
        self._port = port
        self._peer_id = peer_id
        self._bitfield = None
        
        self._choked = True
        self._interested = False
    
    def set_choked(self):
        self._choked = True
    
    def set_unchoked(self):
        self._choked = False
    
    def set_interested(self):
        self._interested = True
    
    def set_uninterested(self):
        self._interested = False
    
    def is_match(self, ip, host, peer_id):
        return (self._ip == ip and self._host == host and self._peer_id == peer_id)