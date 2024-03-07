import hashlib
import os
from bencodepy import encode

def TorrentHash(file_path, piece_length=524288):  # piece_length = 512 KB by default
    """
    Create a BitTorrent info hash for a single file.

    :param file_path: Path to the file to be shared.
    :param piece_length: Length of each piece in bytes (default is 512 KB).
    :return: The SHA-1 hash of the bencoded "info" dictionary, as a hexadecimal string.
    """
    # Initialize the info dictionary
    info = {
        'name': os.path.basename(file_path),
        'length': os.path.getsize(file_path),
        'piece length': piece_length,
        'pieces': b''  # Placeholder for pieces' SHA-1 hashes
    }

    # Read the file and calculate piece hashes
    with open(file_path, 'rb') as file:
        piece_hashes = []
        while True:
            piece = file.read(piece_length)
            if not piece:
                break
            piece_hashes.append(hashlib.sha1(piece).digest())
        info['pieces'] = b''.join(piece_hashes)

    # Bencode the "info" dictionary and calculate the info hash
    bencoded_info = encode(info)
    info_hash = hashlib.sha1(bencoded_info).hexdigest()

    # The info_hash is what's typically used as the torrent's unique identifier
    return info_hash

# Example usage
file_path = 'path/to/your/file.ext'
torrent_hash = create_torrent_hash(file_path)
print(f'Torrent Hash (Info Hash): {torrent_hash}')
