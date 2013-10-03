#!/usr/bin/env python
import bencode
import os
import urllib2
from helpers.torrentfile import TorrentFile
from helpers.tracker import Tracker


filepath = '/sandbox/hackerschool/related_assets'
filename = 'how_to_start_working_as_freelance_web_designer.torrent'

def main():
    file = os.path.join(filepath, filename)
    
    # get torrent file data
    torrentfile = TorrentFile(file)
    digested_info_hash = torrentfile.get_info_hash().digest()
    url = torrentfile.get_tracker_request_url()
    handshake = torrentfile.get_handshake()
    
    # tracker
    tracker = Tracker(url)
    tracker_response = tracker.get_response()
    
    peers_list = tracker.get_peers_list()
    tracker.add_peers(peers_list)
    
    tracker.peers.peers[3].connect(handshake)
    """
    for peer in tracker.peers.peers:
        handshake = peer.get_handshake(PEER_ID, digested_info_hash)
        peer.connect(handshake)
    """
    
    
if __name__ == "__main__":
    main()