// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BitNoahBridge {
    // Structure to hold torrent and IPFS information
    struct TorrentIPFSMapping {
        string torrentHash; // Could be the torrent file hash or magnet link
        string ipfsCID; // IPFS Content Identifier
    }

    // Mapping from torrent hash to its IPFS CID and additional metadata
    mapping(string => TorrentIPFSMapping) public torrentMappings;

    // Event to emit when a new mapping is added
    event MappingAdded(string torrentHash, string ipfsCID);

    // Function to add a new torrent to IPFS mapping
    function addMapping(string memory torrentHash, string memory ipfsCID) public {
        TorrentIPFSMapping memory newMapping = TorrentIPFSMapping({
            torrentHash: torrentHash,
            ipfsCID: ipfsCID
        });

        torrentMappings[torrentHash] = newMapping;
        emit MappingAdded(torrentHash, ipfsCID);
    }

    // Function to retrieve an IPFS CID given a torrent hash
    function getIPFSCID(string memory torrentHash) public view returns (string memory) {
        return torrentMappings[torrentHash].ipfsCID;
    }
}
