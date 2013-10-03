#!/usr/bin/env python
import bencode
import os
import urllib2
from helpers.torrentfile import TorrentFile
from helpers.tracker import Tracker
from helpers.handshake import get_handshake, unpack_handshake


filepath = '/sandbox/hackerschool/related_assets'
filename = 'how_to_start_working_as_freelance_web_designer.torrent'

def main():
    file = os.path.join(filepath, filename)
    
    # get torrent file data
    torrentfile = TorrentFile(file)
    digested_info_hash = torrentfile.get_info_hash().digest()
    url = torrentfile.get_tracker_request_url()
    handshake = get_handshake(digested_info_hash)
    
    # tracker
    tracker = Tracker(url, handshake)
    tracker_response = tracker.get_response()
    
    peers_list = tracker.get_peers_list()
    tracker.add_peers(peers_list)
    
    
    # TODO -- remove the lines below
    peer = tracker.peers.peers[0]
    peer.message.connect()
    
    received_handshake = peer.message.get_peer_handshake()
    msg_length = peer.message.get_msg_length()
    msg = peer.message.get_msg(msg_length)
    peer.message.handle_msg(msg)
    
    # TODO -- uncomment lines below
    # for peer in tracker.peers.peers:
    #         peer.connect(handshake)
    
    
    
    #pstrlen, pstr, reserved_bytes, info_hash, peer_id = unpack_handshake(recv_handshake)
    
    
    
    
    
if __name__ == "__main__":
    main()