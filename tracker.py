from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.web.client import Agent, readBody

from bencode import bdecode
from urllib import urlencode

from peer import Peer, get_peer_ipaddress_and_port


class Tracker(object):
    def __init__(self, peer_id, torrentfile):
        self.peer_id = peer_id
        self.torrentfile = torrentfile
        self.interval = None
        self.min_interval = None


    def tracker_request_url(self, peer_id, torrentfile):
        qs = urlencode({
            'peer_id': peer_id,
            'info_hash': torrentfile.info_hash,
            'left': torrentfile.total_file_length,
        })
        return '?'.join([torrentfile.announce, qs])


    def get_peers_and_connect(self, peer_id, torrentfile, master_control):
        def handle_response_body(body):
            data = bdecode(body)
            self.min_interval = data.get('min interval')
            self.interval = data.get('interval')  

            peers = self.get_peers(data['peers'])          
            for peer in peers:
                master_control.add_peer_connection(peer)
                
                # connect to peer and pass master_control to peer connection
                peer.connect(master_control)

        def handle_request(response):
            d = readBody(response)
            d.addCallback(handle_response_body)

        def handle_request_err(_):
            print 'called handle_request_err'
            reactor.stop()

        agent = Agent(reactor)
        tracker_request_url = self.tracker_request_url(peer_id, torrentfile)
        d = agent.request('GET', tracker_request_url)
        d.addCallbacks(handle_request, handle_request_err)


    def get_peers(self, peers_data):
        peers = []

        # peers data is a list of peers dict
        if isinstance(peers_data, list):
            for peer_data in peers_data:
                peer = Peer(peer_data['ip'], peer_data['port'], self.peer_id)
                peers.append(peer)
        else:
            while peers_data:
                ip, port = get_peer_ipaddress_and_port(peers_data[:6])
                peer = Peer(ip, port, self.peer_id)
                peers.append(peer)

                # remove first 6 bytes (already consumed)
                peers_data = peers_data[6:]

        return peers