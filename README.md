# pyttorrent 
"pit-torrent"



ABOUT
----
BitTorrent client written in Python using the Twisted framework

For now, it deals with single file torrents...but stay tuned!



INSTALL
----
Use pip to install requirements (virtualenv recommended)

    pip install -r requirement.txt




RUN
----
Run the BitTorrent client

    python main.py -f <path/to/torrent/file> -d <path/to/download/directory>



TODOs
----
* Send multiple requests to a peer (pipelining)

* Multi-file torrent
    * Parse file structure
    * Create files based on described file structure
    * Write to multiple files asynchronously
    * Check info hash that span across multiple files

* Large files
    * Request small block sizes (w/ offsets)

