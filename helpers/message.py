"""
Class to handle BitTorrent messages 
<length prefix><message ID><payload>
"""
import socket
import struct

MSG_LENGTH = 4

ID_CHOKE = 0
ID_UNCHOKE = 1
ID_INTERESTED = 2 
ID_NOT_INTERESTED =3 
ID_HAVE = 4
ID_BITFIELD = 5
ID_REQUEST = 6
ID_PIECE = 7
ID_CANCEL = 8
ID_PORT = 9

class Message(object):
    def __init__(self, ip, port, handshake):
        self.ip = ip
        self.port = port
        self.handshake = handshake
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.sock.connect((self.ip, self.port))
        
    def get_peer_handshake(self):
        sent_buffer_size = self.sock.send(self.handshake)
        recv_handshake = self.sock.recv(sent_buffer_size)
        return recv_handshake
        
    def compare_info_hash(self):
        # TODO -- compare received handshake against our info_hash handshake
        pass
        
    def get_msg_length(self):
        msg_length = 0
        recv_bytes = self.sock.recv(MSG_LENGTH)
        
        msg_length += struct.unpack('B', recv_bytes[0])[0] * (256 ^ 3)
        msg_length += struct.unpack('B', recv_bytes[1])[0] * (256 ^ 2)
        msg_length += struct.unpack('B', recv_bytes[2])[0] * (256 ^ 1)
        msg_length += struct.unpack('B', recv_bytes[3])[0]
        
        return msg_length
        
    def get_msg(self, msg_len):
        msg = self.sock.recv(msg_len)
        return msg
        
    def get_msg_id_payload(self, msg):
        msg_id = struct.unpack('B', msg[0])[0]
        payload = msg[1:]
        return msg_id, payload
        
    def handle_msg(self, msg):
        msg_id, payload = self.get_msg_id_payload(msg)
        
        if ID_CHOKE == msg_id:
            self.handle_choke(payload)
            return
        elif ID_UNCHOKE == msg_id:
            self.handle_unchoke(payload)
            return
        elif ID_INTERESTED == msg_id:
            self.handle_interested(payload)
            return
        elif ID_NOT_INTERESTED == msg_id:
            self.handle_not_interested(payload)
            return
        elif ID_HAVE == msg_id:
            self.handle_have(payload)
            return
        elif ID_BITFIELD == msg_id:
            self.handle_bitfield(payload)
            return
        elif ID_REQUEST == msg_id:
            self.handle_request(payload)
            return
        elif ID_PIECE == msg_id:
            self.handle_piece(payload)
            return
        elif ID_CANCEL == msg_id:
            self.handle_cancel(payload)
            return
        elif ID_PORT == msg_id:
            self.handle_port(payload)
            return
        else:
            return
        
    def handle_choke(self, payload):
        pass
    
    def handle_unchoke(self, payload):
        pass
        
    def handle_interested(self, payload):
        pass
    
    def handle_not_interested(self, payload):
        pass

    def handle_have(self, payload):
        pass

    def handle_bitfield(self, payload):
        pass
        
    def handle_request(self, payload):
        pass
        
    def handle_piece(self, payload):
        pass
    
    def handle_cancel(self, payload):
        pass
        
    def handle_port(self, payload):
        pass