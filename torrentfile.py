from bitstring import BitArray
from hashlib import sha1
from bencode import bdecode, bencode


class TorrentFile(object):
    def __init__(self, file_path):
        f = open(file_path, 'r') # read .torrent file in binary mode
        decoded_torrent_file = bdecode(f.read())

        self.file_path = file_path

        # data from torrent file
        self.announce = decoded_torrent_file['announce']
        self.info = decoded_torrent_file['info']
        self.filename = decoded_torrent_file['info']['name']
        self.length = decoded_torrent_file['info']['length']
        self.piece_length = decoded_torrent_file['info']['piece length']
        self.pieces = decoded_torrent_file['info']['pieces']

        self.total_pieces = len(self.pieces) / 20

        # will be zero if the last piece fits perfectly
        #   otherwise will represent the final piece_length in bytes
        self.leftover_piece_length = self.length % self.piece_length

        # set bitfield
        bitstring = '1' * self.total_pieces
        if self.leftover_piece_length > 0:
            bitstring += '0' # padded last piece because it has an incomplete piece size
        self.bitfield = BitArray(bin=bitstring)

    @property
    def info_hash(self):
        return sha1(bencode(self.info)).digest()

    @property
    def total_file_length(self):
        #TODO handle multiple-file torrents
        return self.info['length']

    def get_piece_info_hash(self, piece_index):
        return self.pieces[ piece_index*20 : (piece_index+1)*20 ]

    def __str__(self):
        msg = "announce=%s\nfilename=%s\npiece_length=%d\ntotal_file_length=%d"
        return msg % (self.announce, self.filename, 
            self.piece_length, self.total_file_length)