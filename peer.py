import struct

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.defer import Deferred

class Peer(object):
    def __init__(self, ip, port, torrentfile):
        self.ip = ip
        self.port = port
        self.torrentfile = torrentfile
        self.buffer = ''

    def handle_connection(self):
        def handle_connection_request(self):
            import ipdb
            ipdb.set_trace()
            print 'handle connection request called'

        def handle_connection_failure(self):
            print 'peer connection failure called'

        d = self.get_connection_deferred()
        d.addCallbacks(handle_connection_request, handle_connection_failure)

    def get_connection_deferred(self):
        d = Deferred()
        factory = PeerClientFactory(d)
        print 'connecting to'
        print self.ip, self.port
        
        reactor.connectTCP(self.ip, self.port, factory)
        return d


class PeerProtocol(Protocol):
    def dataReceived(self, data):
        print 'data was received'

    def connectionLost(self, reason):
        print 'connection was lost reason=%r' % (reason,)


class PeerClientFactory(ClientFactory):
    protocol = PeerProtocol
    
    def __init__(self, deferred):
        self.deferred = deferred

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)


def get_peer_ipaddress(bytes):
    ip_addr = [str(struct.unpack('B', byte)[0]) for byte in bytes]
    return '.'.join(ip_addr)


def get_peer_port(bytes):
    return struct.unpack('B', bytes[0])[0] * 256 + struct.unpack('B', bytes[1])[0]


def get_peer_ipaddress_and_port(bytes):
    ip_addr = get_peer_ipaddress(bytes[:4])
    port = get_peer_port(bytes[4:])
    return ip_addr, port