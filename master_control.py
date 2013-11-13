import time

from bitstring import BitArray

from handshake import Handshake


ID_KEEPALIVE = -1
ID_CHOKE = 0
ID_UNCHOKE = 1
ID_INTERESTED = 2 
ID_NOT_INTERESTED =3 
ID_HAVE = 4
ID_BITFIELD = 5
ID_REQUEST = 6
ID_PIECE = 7
ID_CANCEL = 8
ID_PORT = 9


class MasterControl(object):
    def __init__(self, peer_id, torrentfile):
        self.peer_id = peer_id
        self.torrentfile = torrentfile
        self.curr_bitfield = BitArray(bin='0' * len(torrentfile.bitfield.bin))
        self.peer_connections = []
        print 'Master control was created'

    def add_peer_connection(self, peer):
        peer_connection = PeerConnection(peer.ip, peer.port)
        self.peer_connections.append(peer_connection)

    def get_peer_connection(self, peer_protocol):
        peer = peer_protocol.transport.getPeer()
        ip = peer.host
        port = peer.port 
        
        for pc in self.peer_connections:
            if pc.ip == ip and pc.port == port:
                return pc
        return None

    def handle_connection_made(self, peer_protocol):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.protocol = peer_protocol
        peer_connection.connected = True
        
        # send handshake
        handshake = Handshake(peer_id=self.peer_id, 
                              info_hash=self.torrentfile.info_hash)
        peer_connection.send_data(str(handshake))
        
    def handle_connection_lost(self, peer_protocol):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.connected = False
    
    def is_valid_handshake(self, peer_handshake):
        return self.torrentfile.info_hash == peer_handshake.info_hash
    
    def handle_invalid_handshake(self, peer_protocol):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_protocol.loseConnection()
        del peer_connection
    
    def handle_valid_handshake(self, peer_protocol):
        peer_protocol.handshake_received()
    
    def handle_messages(self, peer_protocol, messages):
        for message in messages:
            callback = self.get_callback(message.id)
            callback(peer_protocol, message.payload)
    
    def get_callback(self, message_id):
        if message_id == ID_KEEPALIVE:
            return self.handle_keepalive
        elif message_id == ID_CHOKE:
            return self.handle_choke
        elif message_id == ID_UNCHOKE:
            return self.handle_unchoke
        elif message_id == ID_INTERESTED:
            return self.handle_interested
        elif message_id == ID_NOT_INTERESTED:
            return self.handle_not_interested
        elif message_id == ID_HAVE:
            return self.handle_have
        elif message_id == ID_BITFIELD:
            return self.handle_bitfield
        elif message_id == ID_REQUEST:
            return self.handle_request
        elif message_id == ID_PIECE:
            return self.handle_piece
        elif message_id == ID_PORT:
            return self.handle_port
        else:
            raise Exception('Message id=%d not handled' % (message_id))
    
    
    def handle_keepalive(self, peer_protocol, msg_payload):
        print 'called handle_keep_alive %r' % (peer_protocol.transport.getPeer())
        pass
    
    def handle_choke(self, peer_protocol, msg_payload):
        print 'called handle_choke %r' % (peer_protocol.transport.getPeer())
        pass

    def handle_unchoke(self, peer_protocol, msg_payload):
        print 'called handle_unchoke %r' % (peer_protocol.transport.getPeer())
        pass

    def handle_interested(self, peer_protocol, msg_payload):
        print 'called handle_interested %r' % (peer_protocol.transport.getPeer())
        pass

    def handle_have(self, peer_protocol, msg_payload):
        print 'called handle_have %r' % (peer_protocol.transport.getPeer())
        pass

    def handle_bitfield(self, peer_protocol, msg_payload):
        print 'called handle_bitfield %r' % (peer_protocol.transport.getPeer())
        pass

    def handle_request(self, peer_protocol, msg_payload):
        print 'called handle_request %r' % (peer_protocol.transport.getPeer())
        pass

    def handle_piece(self, peer_protocol, msg_payload):
        print 'called handle_piece %r' % (peer_protocol.transport.getPeer())
        pass

    def handle_port(self, peer_protocol, msg_payload):
        print 'called handle_port %r' % (peer_protocol.transport.getPeer())
        pass



class PeerConnection(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.protocol = None

        self.connected = False
        self.choked = True
        self.last_message = None

    def reset(self):
        self.connected = False
        self.choked = True
        self.last_message = None

    def send_data(self, data):
        self.last_message = time.time()
        self.protocol.send_data(data)
