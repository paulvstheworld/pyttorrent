from bencode import bdecode, bencode
from urllib import urlencode
import hashlib

PEER_ID = '-HS0001-123456789027'

class TorrentFile(object):
    def __init__(self, filepath, peer_id):
        self.filepath = filepath
        
        self.title = ''
        self.announce = ''
        
        self.info = None
        
        self.pieces = ''
        self.piece_length = None
        
        self.filename = ''
        self.files = []
        
        self.peer_id = peer_id
        
    def get_decoded_info(self):
        f = open(self.filepath, 'rb') # read file in binary mode
        decoded_torrent_info = bdecode(f.read()) 
        return decoded_torrent_info
    
    def set_info(self, decoded_torrent_info):
        self.title = decoded_torrent_info['title']
        self.announce = decoded_torrent_info['announce']
        
        self.info = decoded_torrent_info['info']
        self.filename = self.info['name']
        self.files = self.info['files']
        self.piece_length = self.info['piece length']
        self.pieces = self.info['pieces']
        
    def __str__(self):
        return 'title="%s"\nannounce="%s"\nfilename="%s"\npiece_length=%d\n' % (
                self.title, self.announce, self.filename, self.piece_length)
                
    def get_info_hash(self):
        return hashlib.sha1(bencode(self.info))
        
    def get_total_file_length(self):
        file_length = 0
        
        for file in self.files:
            file_length += file.get('length', 0)
            
        return file_length
        
        
    def get_tracker_request_qs(self):
        return urlencode({
            'peer_id': self.peer_id,
            'info_hash': self.get_info_hash().digest(),
            'left': self.get_total_file_length(),
        })
        
    def get_tracker_request_url(self):
        qs = self.get_tracker_request_qs()
        return '?'.join([self.announce, qs])