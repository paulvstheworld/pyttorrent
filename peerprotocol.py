from twisted.internet.protocol import Protocol, ClientFactory

class PeerProtocol(Protocol):
    def dataReceived(self, data):
        msg = "message received: got %d bytes of data from %s"
        print msg % (len(data), self.transport.getPeer())
        
    def connectionLost(self, reason, connector):
        print "lost connection"
        
    def connectionMade(self):
        print "connection made %s" % self.transport.getPeer()



class PeerClientFactory(ClientFactory):
    protocol = PeerProtocol
    
    def __init__(self, client):
        self._client = client

    def buildProtocol(self, address):
        proto = ClientFactory.buildProtocol(self, address)
        proto.peer = 
        return proto
        
    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed', connector, reason