import struct
import time

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.defer import Deferred

from handshake import parse_handshake

from message import parse_message


class Peer(object):
    def __init__(self, ip, port, peer_id):
        self.ip = ip
        self.port = port
        self.peer_id = peer_id

    def connect(self, master_control):
        factory = PeerProtocolFactory(master_control)
        reactor.connectTCP(self.ip, self.port, factory)


class PeerProtocol(Protocol):
    def __init__(self):
        self._buffer = ''
        self.shook_hand = False
        self.master_control = None

    def dataReceived(self, data):
        self._buffer += data

        if not self.shook_hand:
            peer_handshake, self._buffer = parse_handshake(self._buffer)
            if peer_handshake:
                # if successful, will set shook hands to true
                if not self.master_control.is_valid_handshake(peer_handshake):
                    self.master_control.handle_invalid_handshake(self)
                    return

                self.master_control.handle_valid_handshake(self)

                # parse buffer for messages
                msgs, self._buffer = parse_message(self._buffer)
                self.master_control.handle_messages(self, msgs)

        # parse buffer for messages
        else:
            msgs, self._buffer = parse_message(self._buffer)
            self.master_control.handle_messages(self, msgs)

    def connectionMade(self):
        self.master_control.handle_connection_made(self)

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

    def __init__(self, master_control):
        self.master_control = master_control

    def buildProtocol(self, address):
        proto = ClientFactory.buildProtocol(self, address)
        proto.master_control = self.master_control
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