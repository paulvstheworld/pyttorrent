import math
import struct

from bitstring import BitArray


MSG_LENGTH_SIZE = 4

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
    def __init__(self, peer):
        self.peer = peer
        self._buffer = ''

    def add(self, data):
        self._buffer += data

    def bind_message_handlers(self, deferred):
        print 'consuming'

        if len(self._buffer) < MSG_LENGTH_SIZE:
            return
        
        # get message length
        msg_len_in_bytes = self._buffer[0:MSG_LENGTH_SIZE]
        msg_len = self.get_4_byte_to_decimal(msg_len_in_bytes)
        
        # keep alive message
        if msg_len == 0:
            self.handle_keep_alive(deferred)
            # remove keep alive from message buffer
            self._buffer = self._buffer[4:]
            # continue recursion
            self.bind_message_handlers(deferred)

        # did not receive full message
        if len(self._buffer[1:]) < msg_len:
            return

        msg_body = self._buffer[MSG_LENGTH_SIZE : MSG_LENGTH_SIZE + msg_len]
        msg_id, msg_payload = self.get_msg_id_and_payload(msg_body)

        # remove msg that is about to be handled from buffer
        self._buffer = self._buffer[MSG_LENGTH_SIZE + msg_len:]

        # call specific message handler
        handler = self.get_handler(msg_id)
        handler(msg_len, msg_payload, deferred)

        # recursively call itself until there are no more (full) messages to consume
        self.bind_message_handlers(deferred)

    def is_empty(self):
        return len(self._buffer) > 0

    def get_handshake(self):
        handshake_len = self.get_handshake_len()
        if handshake_len > len(self._buffer):
            return None
        return self._buffer[:handshake_len]

    def get_handshake_len(self):
        pstr_len = struct.unpack('B', self._buffer[0])[0]
        return 49 + pstr_len

    def consume_handshake(self):
        handshake_len = self.get_handshake_len()
        self._buffer = self._buffer[handshake_len:]


    ###### HANDLER METHODS ######
    def get_handler(self, msg_id):
        if ID_CHOKE == msg_id:
            return self.handle_choke
        elif ID_UNCHOKE == msg_id:
            return self.handle_unchoke
        elif ID_INTERESTED == msg_id:
            return self.handle_interested
        elif ID_NOT_INTERESTED == msg_id:
            return self.handle_not_interested
        elif ID_HAVE == msg_id:
            return self.handle_have
        elif ID_BITFIELD == msg_id:
            return self.handle_bitfield
        elif ID_REQUEST == msg_id:
            return self.handle_request
        elif ID_PIECE == msg_id:
            return self.handle_piece
        elif ID_CANCEL == msg_id:
            return self.handle_cancel
        elif ID_PORT == msg_id:
            return self.handle_port
        else:
            raise Exception("Unknown message id=%d" % (msg_id,) )

    def handle_keep_alive(self, deferred):
        print 'called handle_keep_alive'

    def handle_choke(self, msg_len, payload, deferred):
        print 'called handle_choke'

    def handle_unchoke(self, msg_len, payload, deferred):
        print 'called handle_unchoke'

    def handle_interested(self, msg_len, payload, deferred):
        print 'called handle_interested'

    def handle_not_interested(self, msg_len, payload, deferred):
        print 'called handle_not_interested'

    def handle_have(self, msg_len, payload, deferred):
        print 'handle_have'
        piece_index = self.get_4_byte_to_decimal(payload)
        self.peer.bitfield[piece_index] = True

    def handle_bitfield(self, msg_len, payload, deferred):
        print 'handle_bitfield'
        self.peer.bitfield = BitArray(bytes=payload)

    def handle_request(self, msg_len, payload, deferred):
        print 'handle_request'

    def handle_piece(self, msg_len, payload, deferred):
        print 'handle_piece'

    def handle_cancel(self, msg_len, payload, deferred):
        print 'handle_cancel'

    def handle_port(self, msg_len, payload, deferred):
        print 'handle_port'


    ###### UTILITY METHODS ######
    def get_msg_id_and_payload(self, msg):
        msg_id = struct.unpack('B', msg[0])[0]
        payload = msg[1:]
        return msg_id, payload

    def get_4_byte_to_decimal(self, msg):
        msg_len = 0
        msg_len += struct.unpack('B', msg[0])[0] * int(math.pow(256, 3))
        msg_len += struct.unpack('B', msg[1])[0] * int(math.pow(256, 2))
        msg_len += struct.unpack('B', msg[2])[0] * int(math.pow(256, 1))
        msg_len += struct.unpack('B', msg[3])[0]

        return msg_len