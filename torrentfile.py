from hashlib import sha1
from bencode import bdecode, bencode

class TorrentFile(object):
    def __init__(self, peer_id, filepath):
        f = open(filepath, 'rb') # read file in binary mode
        decoded_torrent_file = bdecode(f.read())
        
        self.peer_id = peer_id
        
        # data from torrent file
        self.announce = decoded_torrent_file['announce']
        self.info = decoded_torrent_file['info']
        self.filename = decoded_torrent_file['info']['name']
        self.piece_length = decoded_torrent_file['info']['piece length']
        self.pieces = decoded_torrent_file['info']['pieces']
        
        self.peers = []

    @property
    def info_hash(self):
        return sha1(bencode(self.info)).digest()
    
    @property
    def total_file_length(self):
        #TODO handle multiple-file torrents
        return self.info['length']
    
    def __str__(self):
        msg = "announce=%s\nfilename=%s\npiece_length=%d\ntotal_file_length=%d"
        return msg % (self.announce, self.filename, 
            self.piece_length, self.total_file_length)
    