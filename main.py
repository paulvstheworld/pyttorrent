#!/usr/bin/env python
import argparse
import os

from client import BitTorrentClient
from twisted.internet import reactor


def parse_args():
    # get filename from the command line argument
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file',
                        help='path to torrent file',
                        required=True,
                        dest='file',
                        type=argparse.FileType('r'))
    
    parser.add_argument('-d', '--dir',
                        help='path to download directory',
                        required=True,
                        dest='dir',
                        type=str)
    
    args = parser.parse_args()
    filename = os.path.abspath(args.file.name)
    download_dir = args.dir
    
    if not os.path.isdir(download_dir):
        parser.error('Download directory must exist.')
        
    return download_dir, filename
    
def main():
    download_dir, filename = parse_args()
    client = BitTorrentClient(reactor, download_dir, filename)
    client.run()
    
if __name__ == "__main__":
    main()