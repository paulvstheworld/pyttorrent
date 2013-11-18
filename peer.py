import struct
import time

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.defer import Deferred

from bitstring import BitArray

from handshake import parse_handshake
from message import parse_message


class Peer(object):
    def __init__(self, ip, port, peer_id):
        self.ip = ip
        self.port = port
        self.peer_id = peer_id

    def connect(self, client):
        factory = PeerProtocolFactory(client)
        reactor.connectTCP(self.ip, self.port, factory)


class PeerConnection(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.protocol = None

        self.bitfield = BitArray()
        self.connected = False
        self.choked = True
        self.interested = False
        self.last_message = None
        self.piece_requested = None

    def reset(self):
        self.connected = False
        self.choked = True
        self.last_message = None
        self.interested = False
        self.requested_piece = None

    def send_data(self, data):
        self.last_message = time.time()
        self.protocol.send_data(data)

    def finished(self):
        self.protocol.finished()


class PeerProtocol(Protocol):
    def __init__(self):
        self._buffer = ''
        self.shook_hand = False
        self.client = None

    def dataReceived(self, data):
        self._buffer += data

        if not self.shook_hand:
            peer_handshake, self._buffer = parse_handshake(self._buffer)
            if peer_handshake:
                # if successful, will set shook hands to true
                if not self.client.is_valid_handshake(peer_handshake):
                    self.client.handle_invalid_handshake(self)
                    return

                self.client.handle_valid_handshake(self)

                # parse buffer for messages
                msgs, self._buffer = parse_message(self._buffer)
                self.client.handle_messages(self, msgs)

        # parse buffer for messages
        else:
            msgs, self._buffer = parse_message(self._buffer)
            self.client.handle_messages(self, msgs)

    def connectionMade(self):
        print self.transport.getPeer()
        self.client.handle_connection_made(self)

    def connectionLost(self, reason):
        print "connection lost %r %s" % (self.transport.getPeer(), reason)

    def send_data(self, data):
        self.transport.write(data)

    def handshake_received(self):
        self.shook_hand = True
    
    def finished(self):
        reactor.stop()


class PeerProtocolFactory(ClientFactory):
    protocol = PeerProtocol

    def __init__(self, client):
        self.client = client

    def buildProtocol(self, address):
        proto = ClientFactory.buildProtocol(self, address)
        proto.client = self.client
        return proto


def get_peer_ipaddress(bytes):
    ip_addr = [str(struct.unpack('B', byte)[0]) for byte in bytes]
    return '.'.join(ip_addr)


def get_peer_port(bytes):
    return struct.unpack('B', bytes[0])[0] * 256 + struct.unpack('B', bytes[1])[0]


def get_peer_ipaddress_and_port(bytes):
    ip_addr = get_peer_ipaddress(bytes[:4])
    port = get_peer_port(bytes[4:])
    return ip_addr, port