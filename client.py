import time
from torrentfile import TorrentFile

class BitTorrentClient(object):
    def __init__(self, file_location, download_dir):
        self.peer_id =  "-PTW727-"+str(int(time.time())).zfill(12)
        self.file_location = file_location
        self.download_dir = download_dir
        self.torrentfile = TorrentFile(self.peer_id, file_location)
    