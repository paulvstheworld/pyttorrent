#!/usr/bin/env python
import argparse
import bencode
import os
import sys
import urllib2

from lib.handshake import HandShake
from lib.torrentfile import TorrentFile
from lib.tracker import Tracker


def main():
    # get filename from the command line argument
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file',
                        required=True,
                        dest = 'file',
                        type = argparse.FileType('r'))
    
    args = parser.parse_args()
    filename = os.path.abspath(args.file.name)
    
    # get torrent file data
    torrentfile = TorrentFile(filename)
    info_hash = torrentfile.info_hash
    url = torrentfile.get_tracker_request_url()
    pieces = torrentfile.pieces
    
    """
    create proper files and directories
    """
    """
    downloading_file = os.path.abspath('../related_assets/downloads/%s' % torrentfile.filename)
    file = open(downloading_file, 'wb')
    f.write(bin_data)
    """
    
    
    
    
    # client_handshake
    client_handshake = HandShake()
    client_handshake.set_default_values(torrentfile.info_hash)
    
    # tracker
    tracker = Tracker(url, str(client_handshake))
    tracker_response = tracker.get_response()
    
    # add peers to the tracker peers collection
    peers_list = tracker.get_peers_list()
    tracker.add_peers(peers_list)
    
    """
    TODO -- remove the lines below
    """ 
    peer = tracker.get_peer_by_ip_port('96.126.104.219', 65373)
    peer.connection.open()
    peer.connection.send_data(str(client_handshake))
    
    # create peer handshake instance
    peer_handshake_string = peer.connection.recv_data()
    peer_handshake = HandShake()
    peer_handshake.set_handshake_data_from_string(peer_handshake_string)
    
    data = peer.connection.recv_data()
    peer.append_to_buffer(data)
    peer.consume_messages()
    
    import ipdb
    ipdb.set_trace()
    
    peer.connection.send_interested()
    data = peer.connection.recv_data()
    peer.append_to_message_buffer(data)
    peer.consume_message_buffer()
    
    """
    for i in range(0, 79):
        peer.connection.send_request(i)
        data = peer.connection.recv_data()
        peer.append_to_message_buffer(data)
        peer.consume_message_buffer()
    """
    
    peer.connection.send_request(0)
    data = peer.connection.recv_data()
    peer.append_to_message_buffer(data)
    peer.consume_message_buffer()
    
    
if __name__ == "__main__":
    main()