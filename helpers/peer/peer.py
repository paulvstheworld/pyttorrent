from helpers.message import Message

class Peer(object):
    def __init__(self, ip, port, handshake, id=''):
        self.ip = ip
        self.port = port
        self.id = id
        self.status = None
        self.sock = None
        
        # TODO -- remove lines below (hardcoded values)
        self.ip = '41.224.255.137'  
        self.port = 63388
        
        self.message = Message(self.ip, self.port, handshake)
    