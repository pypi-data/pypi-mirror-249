from pathlib import Path
from hashlib import md5

def _check_integrity(path, hash_, calculate_hash):
    """
    :args:
        path (str):
        hash_ (str): expected hash of file
        calculate_hash (callable): function to calculate hash
    """
    if not Path(path).is_file():
        return False

    if calculate_hash(path) == hash_:
        return True
    else:
        return False

def _calculate_md5(path):
    """
    :args:
        path (str):
    """
    with open(path, 'rb') as f:
        bytes = f.read()
        hash_ = md5(bytes)

    return hash_.hexdigest()
