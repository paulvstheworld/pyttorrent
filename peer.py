import struct
import time

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.defer import Deferred

from handshake import Handshake
from message import Message


class Peer(object):
    def __init__(self, ip, port, torrentfile):
        self.ip = ip
        self.port = port
        self.peer_id = torrentfile.peer_id
        self.torrentfile = torrentfile
        
        self.connector = None
        self.connected = None
        
        # peer properties
        self.bitfield = None
        
        # timestamp
        self.timestamp_last_message_sent = None
        
        # flags
        self.received_handshake = False
        self.choked = True


    def setup_connection(self):
        def handle_connection_request(self):
            print 'handle connection request called'

        def handle_connection_failure(self):
            print 'peer connection failure called'

        d = self.get_connection_deferred()
        d.addCallbacks(handle_connection_request, handle_connection_failure)


    def get_connection_deferred(self):
        d = Deferred()
        factory = PeerClientFactory(self, d)
        self.connector = reactor.connectTCP(self.ip, self.port, factory)
        return d


    def mark_message_timestamp(self):
        self.timestamp_last_message_sent = time.time()

    def is_correct_info_hash(self, peer_handshake):
        return peer_handshake.info_hash == self.torrentfile.info_hash


class PeerProtocol(Protocol):
    def dataReceived(self, data):
        print 'data=%s' % data
        self.factory.handle_data(data)

    def connectionMade(self):
        handshake_str = str(self.factory.get_handshake())
        self.send_message(handshake_str)
        print 'sent peer handshake'

    def connectionLost(self, reason):
        print self.transport.getPeer()
        print 'connection was lost reason=%r' % (reason,)

    def send_message(self, msg):
        self.transport.write(msg)
        self.factory.peer.mark_message_timestamp()


class PeerClientFactory(ClientFactory):
    protocol = PeerProtocol

    def __init__(self, peer, deferred):
        self.peer = peer
        self.message = Message(self.peer)
        self.deferred = deferred

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)

    def get_handshake(self):
        peer_id = self.peer.peer_id
        info_hash = self.peer.torrentfile.info_hash
        handshake = Handshake(peer_id=peer_id, info_hash=info_hash)
        return handshake

    def handle_data(self, data):
        self.message.add(data)

        if not self.peer.received_handshake:
            peer_handshake = self.message.get_handshake()
            if not peer_handshake:
                return

            # check peer handshake info hash
            peer_handshake = Handshake(handshake_str=peer_handshake)
            if not self.peer.is_correct_info_hash(peer_handshake):
                self.peer.connector.disconnect()
                return

            self.message.consume_handshake()
            self.peer.received_handshake = True

            # attempt to consume any remaining messages
            if not self.message.is_empty():
                self.message.bind_message_handlers(self.deferred)
        else:
            self.message.bind_message_handlers(self.deferred)


def get_peer_ipaddress(bytes):
    ip_addr = [str(struct.unpack('B', byte)[0]) for byte in bytes]
    return '.'.join(ip_addr)


def get_peer_port(bytes):
    return struct.unpack('B', bytes[0])[0] * 256 + struct.unpack('B', bytes[1])[0]


def get_peer_ipaddress_and_port(bytes):
    ip_addr = get_peer_ipaddress(bytes[:4])
    port = get_peer_port(bytes[4:])
    return ip_addr, port