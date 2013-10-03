import socket

AM_CHOKING  = 1         # this client is choking the peer
AM_INTERESTED = 0       # this client is interested in the peer
PEER_CHOKING = 1        # peer is choking this client
PEER_INTERESTED =0      # peer is interested in this client


class Peer(object):
    def __init__(self, ip, port, id=''):
        self.ip = ip
        self.port = port
        self.id = id
        self.status = None
        self.sock = None
    
    
    def connect(self, handshake):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        
        # send handshake to peer
        sent_buffer_size = self.sock.send(handshake)
        recv = self.sock.recv(sent_buffer_size)
        
        self.sock.close()
        
        print recv
        