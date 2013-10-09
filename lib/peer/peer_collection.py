class PeerCollection(object):
    def __init__(self):
        self.peers = []
    
    def add(self, peer):
        self.peers.append(peer)
    
    def get_peer_by_ip_port(self, ip, port):
        for peer in self.peers:
            if peer.ip == ip and peer.port == port: 
                return peer
        return None
    
    
    def remove_peer_by_id(self, peer):
        self.peers.remove()
    
    
    def remove_peer_by_ip_addr_and_port(self, ip_addr, port):
        for peer in self.peers:
            if peer.ip_addr == ip_addr and peer.port == port: 
                self.peers.remove(peer)
    
    
    def __str__(self):
        peers = []
        for peer in self.peers:
            peers.append("ip=%16s  port=%6d  id=%s\n" % (peer.ip, peer.port, peer.id))
        
        return ''.join(peers)