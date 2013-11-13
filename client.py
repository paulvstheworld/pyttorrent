import os
import time

from torrentfile import TorrentFile


class BitTorrentClient(object):
    def __init__(self, download_dir):
        self.peer_id = "-PTW727-"+str(int(time.time())).zfill(12)
        self.download_dir = download_dir
    
    def create_file(self, torrentfile):
        download_file_location = os.path.join(self.download_dir, torrentfile.filename)

        if os.path.exists(download_file_location):
            return

        file = open(download_file_location, 'w+')
