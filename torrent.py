from peer import Peer

class Torrent(object, peer_id):
    def __init__(self):
        self.peer_id = peer_id
        self._peers = []
    
    def add_peers(self, peers_list):
        for peer_obj in peers_list:
            peer = Peer(peer['ip'], peer['port'], self.peer_id)
            self._peers.append(peer)
    
    def get_peer(self, ip, host, peer_id):
        for peer in self._peers:
            if peer.is_match(ip, host, peer_id):
                return peer
        return None