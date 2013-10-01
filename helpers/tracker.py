import bencode
import struct
import urllib2

BLOCK_SIZE = 6

class Tracker(object):
    def __init__(self, requesturl):
        self.requesturl = requesturl
        self.decoded_response = None
        self.peers_list = []
    
    def get_response(self):
        response = urllib2.urlopen(self.requesturl).read()
        self.decoded_response = bencode.bdecode(response)
        return self.decoded_response
    
        
    def has_binary_peers(self):
        peers = self.decoded_response['peers']
        return not isinstance(peers, list)    
    
    
    def get_peers_list(self):
        if not self.has_binary_peers():
            return self.decoded_response['peers']
        
        return self.get_binary_peers_list()
    
    
    def get_binary_peers_list(self):
        peers_list = []
        peers = self.decoded_response['peers']
        
        index_start = 0
        index_curr = 0
        index_end = len(peers) - 1
        
        while(index_start < index_end):
            # get block
            binary_peer_block = peers[index_start : index_start + BLOCK_SIZE]
            
            # add peer info dictionary to list
            peer_dict = self.get_binary_peer_dict(binary_peer_block)
            peers_list.append(peer_dict)
            
            # increment index start by the next block size
            index_start += BLOCK_SIZE
    
    
    def get_peer_ipaddress(self, bytes):
        ip_addr = []
        ip_addr.append(str(struct.unpack('B', bytes[0])[0]))
        ip_addr.append(str(struct.unpack('B', bytes[1])[0]))
        ip_addr.append(str(struct.unpack('B', bytes[2])[0]))
        ip_addr.append(str(struct.unpack('B', bytes[3])[0]))
        return '.'.join(ip_addr)
    
    
    def get_peer_port(self, bytes):
        return struct.unpack('B', bytes[0])[0] * 256 + struct.unpack('B', bytes[1])[0]
    
    
    def get_binary_peer_dict(self, block):
        return {
            'ip': self.get_peer_ipaddress(block[0:4]),
            'port': self.get_peer_port(block[4:])
        }
        