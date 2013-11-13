#!/usr/bin/env python

import os
import argparse

from twisted.internet import reactor

from client import BitTorrentClient
from master_control import MasterControl
from torrentfile import TorrentFile
from tracker import Tracker

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
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
    torrentfile = TorrentFile(file_location)

    client = BitTorrentClient(download_dir)
    client.create_file(torrentfile)

    master_control = MasterControl(client.peer_id, download_dir, torrentfile)

    tracker = Tracker(client.peer_id, torrentfile)
    tracker.get_peers_and_connect(client.peer_id, torrentfile, master_control)

    reactor.run()


if __name__ == '__main__':
    main()