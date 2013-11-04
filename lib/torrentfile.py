from hashlib import sha1

from bencode import bdecode, bencode
from urllib import urlencode

from lib.handshake import PEER_ID


class TorrentFile(object):
    def __init__(self, filepath):
        f = open(filepath, 'rb') # read file in binary mode
        decoded_torrent_info = bdecode(f.read())
        
        self.announce = decoded_torrent_info['announce']
        self.info = decoded_torrent_info['info']
        self.filename = self.info['name']
        self.piece_length = self.info['piece length']
        self.pieces = self.info['pieces']
        self._info_hash = None
    
    @property
    def info_hash(self):
        return sha1(bencode(self.info)).digest()
    
    def get_total_file_length(self):
        return self.info['length']
    
    def get_tracker_request_qs(self):
        return urlencode({
            'peer_id': PEER_ID,
            'info_hash': self.info_hash,
            'left': self.get_total_file_length(),
        })
    
    def get_tracker_request_url(self):
        qs = self.get_tracker_request_qs()
        return '?'.join([self.announce, qs])
    
    def __str__(self):
        return 'title="%s"\nannounce="%s"\nfilename="%s"\npiece_length=%d\n' % (
                self.title, self.announce, self.filename, self.piece_length)