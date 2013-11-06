from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.web.client import Agent, readBody

from bencode import bdecode
from urllib import urlencode

from peer import Peer
from peer import get_peer_ipaddress_and_port


class Tracker(object):
    def __init__(self, torrentfile):
        self.torrentfile = torrentfile
        self.interval = None
        self.min_interval = None

    @property
    def tracker_request_url(self):
        qs = urlencode({
            'peer_id': self.torrentfile.peer_id,
            'info_hash': self.torrentfile.info_hash,
            'left': self.torrentfile.total_file_length,
        })
        return '?'.join([self.torrentfile.announce, qs])


    def handle_peer_connections(self):
        def handle_response_body(body):
            data = bdecode(body)
            
            self.min_interval = data.get('min interval')
            self.interval = data.get('interval')
            self.add_peers_to_torrentfile(data['peers'])

        def handle_request(response):
            d = readBody(response)
            d.addCallback(handle_response_body)

        def handle_request_err(_):
            print 'called handle_request_err'
            reactor.stop()

        agent = Agent(reactor)
        d = agent.request('GET', self.tracker_request_url)
        d.addCallbacks(handle_request, handle_request_err)


    def add_peers_to_torrentfile(self, peers_data):
        # peers data is a list of peers dict
        if isinstance(peers_data, list):
            for peer_data in peers_data:
                self.add_peer_to_torrentfile_and_connect(peer['ip'], peer['port'])

        # peers data is (in binary mode) byte string
        else:
            while peers_data:
                ip, port = get_peer_ipaddress_and_port(peers_data[:6])
                self.add_peer_to_torrentfile_and_connect(ip, port)
                
                # step to the next 6 bytes
                peers_data = peers_data[6:]


    def add_peer_to_torrentfile_and_connect(self, ip, port):
        peer = Peer(ip, port, self.torrentfile)
        self.torrentfile.peers.append(peer)
        peer.setup_connection()