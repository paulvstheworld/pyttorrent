import struct

from bitstring import BitArray

from utils import get_4_bytes_in_decimal


class Message(object):
    def __init__(self, msg_len=0, id=None, payload=None):
        self.msg_len=msg_len
        self.id=id
        self.payload=payload


def parse_message(buffer):
    return parse_message_helper([], buffer)


def parse_message_helper(messages, buffer):
    _msg_length_size = 4
    
    if len(buffer) < _msg_length_size:
        return messages, buffer

    msg_len = get_4_bytes_in_decimal(buffer[0:_msg_length_size])

    # keep alive message
    if msg_len == 0:
        messages.append(Message(id=ID_KEEPALIVE))
        buffer = buffer[4:]
        return parse_message_helper(messages, buffer)
        
    # incomplete message
    if len(buffer[1:]) < msg_len:
        return messages, buffer

    # complete message
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