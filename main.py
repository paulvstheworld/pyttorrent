#!/usr/bin/env python

import os
import argparse

from twisted.internet import reactor

from client import BitTorrentClient
from torrentfile import TorrentFile
from tracker import Tracker

def parse_args():
    parser = argparse.ArgumentParser(description='Download a small single file via BitTorrent protocol')
    parser.add_argument('-f', '--file',
                        required=True,
                        dest = 'file',
                        type = argparse.FileType('r'))

    parser.add_argument('-d', '--dir',
                        help='path to download directory',
                        required=True,
                        dest='dir',
                        type=str)

    args = parser.parse_args()
    file_location = os.path.abspath(args.file.name)
    download_dir = args.dir

    if not os.path.isdir(download_dir):
        parser.error('Download directory must exist.')

    return file_location, download_dir


def main():
    file_location, download_dir = parse_args()
    
    # parse the torrent file and make into an object
    torrentfile = TorrentFile(file_location)

    # create bittorrent client (brain behind everything)
    client = BitTorrentClient(download_dir, torrentfile)
    client.create_files()

    # create tracker and add it to the client
    tracker = Tracker(client.peer_id, torrentfile)
    client.add_tracker(tracker)

    # connect to the peers associated to the tracker
    tracker.get_peers_and_connect(client, torrentfile)
    
    reactor.run()


if __name__ == '__main__':
    main()
