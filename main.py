#!/usr/bin/env python
import bencode
import os
import urllib2
from helpers.torrentfile import TorrentFile
from helpers.tracker import Tracker


filepath = '/sandbox/hackerschool/related_assets'
filename = 'how_to_start_working_as_freelance_web_designer.torrent'

PEER_ID = '-HS0001-123456789027'

def main():
    file = os.path.join(filepath, filename)
    torrentfile = TorrentFile(file, PEER_ID)
    
    decoded_info = torrentfile.get_decoded_info()
    torrentfile.set_info(decoded_info)
    
    digested_info_hash = torrentfile.get_info_hash().digest()
    
    url = torrentfile.get_tracker_request_url()
    
    tracker = Tracker(url)
    tracker_response = tracker.get_response()
    
    peers_list = tracker.get_peers_list()
    tracker.set_peers(peers_list)
    
    
    for peer in tracker.peers.peers:
        handshake = peer.get_handshake(PEER_ID, digested_info_hash)
        peer.connect(handshake)
    
    
    
if __name__ == "__main__":
    main()