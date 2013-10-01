#!/usr/bin/env python
import bencode
import os
import urllib2
from helpers.torrentfile import TorrentFile
from helpers.tracker import Tracker



filepath = '/Users/paul/Downloads/'
filename = 'how_to_start_working_as_freelance_web_designer.torrent'

def main():
    file = os.path.join(filepath, filename)
    torrentfile = TorrentFile(file)
    
    decoded_info = torrentfile.get_decoded_info()
    torrentfile.set_info(decoded_info)
    
    url = torrentfile.get_tracker_request_url()
    
    tracker = Tracker(url)
    tracker_response = tracker.get_response()
    
    tracker.get_peers_list()
    
    
if __name__ == "__main__":
    main()