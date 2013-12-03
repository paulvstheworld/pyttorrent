# pyttorrent 
"pit-torrent"

BitTorrent client written in Python using the Twisted framework.

For now, it deals with single file torrents...but stay tuned!


INSTALL
----
Use pip to install requirements (virtualenv recommended).

    pip install -r requirement.txt


RUN
----
You want to run the main.py file with (2) arguments.

The path to the torrent file (-f/--file) and the path to the download directory (-d/--dir)

    python main.py -f <path/to/torrent/file> -d <path/to/download/directory>

OR

    python main.py --file=<path/to/torrent/file> --dir=<path/to/download/directory>

Hang back while the torrent downloads.
The program will stop running when the download has completed.


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