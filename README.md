# IPFS BitTorrent Mirror

A python utility to fetch and seed a common dataset to both IPFS and a BitTorrent tracker.

Originally designed to help individuals strengthen the Library Genesis collection, but written to be generally useful for mirroring between networks.

[Read the LibGen IPFS Seeding Guide](https://freeread.org/ipfs/)

## Features

* **filter by minimum seeders**: Prioritize the files that need seeding the most.
* **Set max disk usage**: Set a limit on disk usage
* **Clone a dataset**: Find files from a large dataset where some parts are available from ipfs and others from bittorrent.
* **Mirror from BitTorrent to IPFS** - If you only have a .torrent file, this tool will clone it in IPFS.  However, if you only have a CID, this tool will not create a torrent file.

## How it works

Provide a manifest file (or several) describing pairings between `.torrent` files and IPFS CID hashes.  This tool will iterate the list, attempt to retreive the data from one network, then once it is successfully fetched, propogate it to the other.

It is just a command-line script, not a service, so the user must initiate each "round" of checks.  If a torrent is added to qBitTorrent today and takes 4 hours to dowload, you'll have to come back 4 hours later and run another "round" to collect the newly completed data and pin it to your ipfs node.

Ideally a scheduler like cron or systemd will run a round of checks at intervals

If users all attempt to seed the most-needed files first, eventually the network will be seeded bottom-up.

## Configuration

See `./config.example.json`

## Manifest Schema

Peerfiles are a manifest of torrent/cid pairs that belong to some common group.  Manifests for the project or dataset you want to seed should come from an official community source.

```json
{
    "name": "Libgen SciTech Repository",
    "description": "The main libgen repository",
    "tags": ["scitech"],
    "pairs": [
        {
            "torrent_file": "http://libgen.rs/repository_torrent/r_000.torrent",
            "ipfs_cid": "bafykbzaceaeofefgje22l7rhgtcgs22m32f4ysw5nqa3ty5zawfovqam7pj2c",
        },
        {
            "torrent_file": "http://libgen.rs/repository_torrent/r_1000.torrent",
            "ipfs_cid": "bafykbzacec26l2xeok4xwa3bsuyn5bw7wismuiyudfbgqsozcsicwej4suqhi",
        }
        /* ... */
    ]
}
```

## Prerequisites

* A qBittorrent server
* An ipfs server

If you aren't already running these, you can use the included docker-compose.  If you run these services on your own, you MUST have a shared data volume accessible from both services.
