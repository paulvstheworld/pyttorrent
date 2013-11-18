import struct

from bitstring import BitArray

from utils import get_4_bytes_in_decimal

ID_KEEPALIVE = -1
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
    def __init__(self, msg_len=0, id=None, payload=''):
        self.msg_len=msg_len
        self.id=id
        self.payload=payload
    
    def __str__(self):
        return '%s%s%s' % (self.msg_len, self.id, self.payload,)


def parse_message(buffer):
    return parse_message_helper([], buffer)


def parse_message_helper(messages, buffer):
    _msg_length_size = 4
    
    # check for message length
    if len(buffer) < _msg_length_size:
        return messages, buffer

    msg_len = get_4_bytes_in_decimal(buffer[0:_msg_length_size])

    # keep alive message
    if msg_len == 0:
        messages.append(Message(id=ID_KEEPALIVE))
        buffer = buffer[4:]
        return parse_message_helper(messages, buffer)
        
    # check for incomplete message
    if len(buffer[1:]) < msg_len:
        return messages, buffer

    # consume complete message
    msg_body = buffer[_msg_length_size : _msg_length_size + msg_len]
    id, payload = get_message_id_and_payload(msg_body)
    
    message = Message(msg_len=msg_len, id=id, payload=payload)
    messages.append(message)
    
    # remove parsed message and continue with the rest of the buffer
    buffer = buffer[_msg_length_size + msg_len:]
    return parse_message_helper(messages, buffer)


def get_message_id_and_payload(msg_body):
    msg_id = struct.unpack('B', msg_body[0])[0]
    payload = msg_body[1:]
    return msg_id, payload


def get_interested_message():
    # <len=0001><id=2>
    msg_len = BitArray(uint=1, length=32).bytes
    id = chr(ID_INTERESTED)
    
    return Message(msg_len=msg_len, id=id)


def get_request_piece_message(piece_index, begin, requested_length):
    # <len=0013><id=6><index><begin><length>
    msg_len = BitArray(uint=13, length=32).bytes
    id = chr(ID_REQUEST)
    index = BitArray(uint=piece_index, length=32).bytes
    begin = BitArray(uint=begin, length=32).bytes # block offset
    requested_length = BitArray(uint=requested_length, length=32).bytes # block offset
    payload = '%s%s%s' % (index, begin, requested_length)
    
    return Message(msg_len=msg_len, id=id, payload=payload)