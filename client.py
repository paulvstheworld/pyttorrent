import time

from lib.torrentfile import TorrentFile
from lib.handshake import HandShake
from lib.tracker import Tracker
from peerprotocol import PeerClientFactory

class BitTorrentClient(object):
    def __init__(self, reactor, download_dir, filename):
        self._reactor = reactor
        self._peer_id = "-PTW727-"+str(int(time.time())).zfill(12)
        
        self.filename = filename
        self.download_dir = download_dir
    
    def run(self):
        torrent = Torrent(self._peer_id)
        torrentfile = TorrentFile(self.filename)
        url = torrentfile.get_tracker_request_url()
        
        client_handshake = HandShake()
        client_handshake.set_default_values(torrentfile.info_hash)
        
        tracker = Tracker(url)
        tracker.send_request()
        
        peer_addrs = tracker.get_peers_list()
        
        factory = PeerClientFactory(self)
        
        for peer_addr in peer_addrs:
            torrent.add_peer(peer)
            self._reactor.connectTCP(peer_addr['ip'], peer_addr['port'], factory)
            
        self._reactor.run()