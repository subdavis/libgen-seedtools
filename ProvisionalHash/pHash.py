import hashlib
import bencodepy

def calculate_info_hash(info_dict):
    """
    Calculate the SHA-1 hash of the "info" dictionary from a torrent file,
    given the dictionary has already been loaded into a Python dict.

    :param info_dict: The "info" dictionary from a torrent file.
    :return: The SHA-1 hash of the bencoded "info" dictionary, as a hexadecimal string.
    """
    # Bencode the "info" dictionary
    bencoded_info = bencodepy.encode(info_dict)

    # Calculate SHA-1 hash of the bencoded "info" dictionary
    sha1_hash = hashlib.sha1(bencoded_info).hexdigest()

    return sha1_hash

# Example usage:
# Suppose you have an "info" dictionary loaded into `info_dict`, then you would call:
# hash_result = calculate_info_hash(info_dict)
# print(hash_result)
