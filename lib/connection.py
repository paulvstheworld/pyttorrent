import socket

MAX_BUFFER_SIZE = 4096

class Connection(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def open(self):
        self.socket.connect((self.ip, self.port))
        
    def send_data(self, data):
        self.socket.send(data)
        
    def recv_data(self):
        data = self.socket.recv(MAX_BUFFER_SIZE)
        return data