import os
import time

from bitstring import BitArray
from hashlib import sha1

from handshake import Handshake
from message import get_interested_message, get_request_piece_message
from message import (ID_KEEPALIVE, ID_CHOKE, ID_UNCHOKE, ID_INTERESTED, 
                     ID_NOT_INTERESTED, ID_HAVE, ID_BITFIELD, ID_REQUEST, 
                     ID_PIECE, ID_CANCEL, ID_PORT)

from peer import PeerConnection
from utils import get_4_bytes_in_decimal




class MasterControl(object):
    def __init__(self, peer_id, download_dir, torrentfile):
        self.peer_id = peer_id
        self.download_dir = download_dir
        self.torrentfile = torrentfile
        self.curr_bitfield = BitArray(bin='0' * len(torrentfile.bitfield.bin))
        self.peer_connections = []
        print 'Master control was created'



    ######### PIECE UTILITY METHODS #########
    def has_retrieved_all_pieces(self):
        return self.curr_bitfield == self.torrentfile.bitfield

    def is_piece_valid(self, block, index):
        print 'piece for index=%d is valid' % index
        return sha1(block).digest() == self.torrentfile.get_piece_info_hash(index)

    def request_next_piece(self, peer_connection):
        piece_index = self.get_next_piece_index(peer_connection)

        print 'next needed piece=%d' % piece_index

        piece_length = self.get_piece_length(piece_index)
        self.request_piece(peer_connection, piece_index, 0, piece_length)
        peer_connection.piece_requested = piece_index

    def request_piece(self, peer_connection, piece_index, begin, requested_length):
        piece_message = get_request_piece_message(piece_index, begin, requested_length)
        peer_connection.send_data(piece_message)

    def set_piece_received(self, index):
        self.curr_bitfield[index] = True



    ######### PEER UTILITY METHODS #########

    def add_peer_connection(self, peer):
        peer_connection = PeerConnection(peer.ip, peer.port)
        self.peer_connections.append(peer_connection)

    def get_peer_connection(self, peer_protocol):
        peer = peer_protocol.transport.getPeer()
        ip = peer.host
        port = peer.port 

        for pc in self.peer_connections:
            if pc.ip == ip and pc.port == port:
                return pc
        return None

    def get_piece_length(self, index):
        # check if last piece
        if index == self.torrentfile.total_pieces-1:
            piece_length = self.torrentfile.leftover_piece_length
        else:
            piece_length = self.torrentfile.piece_length

        return piece_length



    ######### CONNECTION HANDLERS #########

    def handle_connection_made(self, peer_protocol):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.protocol = peer_protocol
        peer_connection.connected = True
        
        # send handshake
        handshake = Handshake(peer_id=self.peer_id, 
                              info_hash=self.torrentfile.info_hash)
        peer_connection.send_data(str(handshake))


    def handle_connection_lost(self, peer_protocol):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.connected = False



    ######### HANDSHAKE UTILITY METHODS #########

    def is_valid_handshake(self, peer_handshake):
        return self.torrentfile.info_hash == peer_handshake.info_hash


    def handle_invalid_handshake(self, peer_protocol):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_protocol.loseConnection()
        del peer_connection


    def handle_valid_handshake(self, peer_protocol):
        peer_protocol.handshake_received()



    ######### MESSAGE HANDLERS #########

    def handle_messages(self, peer_protocol, messages):
        for message in messages:
            handler = self.get_handler(message.id)
            handler(peer_protocol, message.payload)

    def get_handler(self, message_id):
        if message_id == ID_KEEPALIVE:
            return self.handle_KEEPALIVE
        elif message_id == ID_CHOKE:
            return self.handle_CHOKE
        elif message_id == ID_UNCHOKE:
            return self.handle_UNCHOKE
        elif message_id == ID_INTERESTED:
            return self.handle_INTERESTED
        elif message_id == ID_NOT_INTERESTED:
            return self.handle_NOT_INTERESTED
        elif message_id == ID_HAVE:
            return self.handle_HAVE
        elif message_id == ID_BITFIELD:
            return self.handle_BITFIELD
        elif message_id == ID_REQUEST:
            return self.handle_REQUEST
        elif message_id == ID_PIECE:
            return self.handle_PIECE
        elif message_id == ID_PORT:
            return self.handle_PORT
        else:
            raise Exception('Message id=%d not handled' % (message_id))


    def handle_KEEPALIVE(self, peer_protocol, msg_payload):
        print 'called handle_keep_alive %r' % (peer_protocol.transport.getPeer())


    def handle_CHOKE(self, peer_protocol, msg_payload):
        print 'called handle_choke %r' % (peer_protocol.transport.getPeer())


    def handle_UNCHOKE(self, peer_protocol, msg_payload):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.choked = False
        self.request_next_piece(peer_connection)


    def handle_INTERESTED(self, peer_protocol, msg_payload):
        print 'called handle_interested %r' % (peer_protocol.transport.getPeer())


    def handle_NOT_INTERESTED(self, peer_protocol, msg_payload):
        print 'called handle_not_interested %r' % (peer_protocol.transport.getPeer())


    def handle_HAVE(self, peer_protocol, msg_payload):
        piece_index = get_4_bytes_in_decimal(msg_payload)
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.bitfield[piece_index] = True        


    def handle_BITFIELD(self, peer_protocol, msg_payload):
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.bitfield = BitArray(bytes=msg_payload)

        # send interested
        self.send_INTERESTED(peer_protocol)
        peer_connection.interested_sent = True


    def handle_REQUEST(self, peer_protocol, msg_payload):
        print 'called handle_request %r' % (peer_protocol.transport.getPeer())


    def handle_PIECE(self, peer_protocol, msg_payload):
        print 'received piece from peer %r' % (peer_protocol.transport.getPeer())
        
        peer_connection = self.get_peer_connection(peer_protocol)
        
        index = get_4_bytes_in_decimal(msg_payload[0:4])
        begin = get_4_bytes_in_decimal(msg_payload[4:8])
        block = msg_payload[8:]
        
        if not self.is_piece_valid(block, index):
            # request piece again
            piece_length = self.get_piece_length(piece_index)
            self.request_piece(peer_connection, index, 0, piece_length)
            peer_connection.piece_requested = index
            return
        
        print 'received piece index=%d' % index
        
        # update which piece was received in master control bitfield
        self.set_piece_received(index)

        # reset requested piece
        peer_connection.piece_requested = None
        
        self.write_to_file(index, begin, block)

        # check if there are more pieces left over
        if self.has_retrieved_all_pieces():
            print 'retrieved all pieces'
            peer_connection.finished()
        else:
            peer_connection = self.get_peer_connection(peer_protocol)
            self.request_next_piece(peer_connection)


    def handle_PORT(self, peer_protocol, msg_payload):
        print 'called handle_port %r' % (peer_protocol.transport.getPeer())


    def get_next_piece_index(self, peer_connection):
        for i, piece in enumerate(self.curr_bitfield):
            if not piece and peer_connection.bitfield[i]:
                return i

        return None



    ######### WRITING TO PEER #########

    def send_INTERESTED(self, peer_protocol):
        interested_msg = get_interested_message()
        peer_connection = self.get_peer_connection(peer_protocol)
        peer_connection.send_data(interested_msg)

    
    def write_to_file(self, index, begin, block):
        filepath = os.path.join(self.download_dir, self.torrentfile.filename)
        file = open(filepath, 'r+b')
        file.seek(index * self.torrentfile.piece_length + begin)
        file.write(block)
        file.close()




