Every time your computer conncets to a swarm, it becomes a peer
Program peers use to access the swam is the BitTorrent client


* Blocks - pieces are split into blocks
  * peers only advertise that they have entire pieces
  * downloading strategy piece (interesting part)

  * leeching
    * peers request blocks from each other
  * seeding
    * deliver those blocks

Steps
=====
* metainfo file
  * BitTorrent client needs to read the metainfo file (.torrent file)
  * contains information about the data file (file you're downloading)
  * contains tracker
    * URI for fetching the list of peers that are currently part of the swarm
  * encoded in bencode (does it need to be decoded?)


* get the announce url and info dictionary
  * within info dictionary
    * get piece length
    * get name
    * pieces (hash list)
    * paths
    * lengths (of all files)

* client must fetch the list of peers from the tracker
* connect to some (or all) of them via handshake