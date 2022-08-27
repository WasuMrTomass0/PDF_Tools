from PIL import Image
import tempfile
import json
import os

import settings


def add_suffix_to_path(path: str, suffix: str) -> str:
    """Add suffix to path - before extension

    Args:
        path (str): Path
        suffix (str): Suffix to append

    Returns:
        str: New path
    """
    if '.' not in path:
        return path + suffix

    parts = path.split('.')
    extension = parts[-1]
    path = '.'.join(parts[:-1])
    return path + suffix + '.' + extension


def get_unused_path(path: str) -> str:
    """Create unused path by appending f'_{i}' to path

    Args:
        path (str): First path

    Returns:
        str: Unused path created by appending number
    """
    if not os.path.isfile(path):
        return path

    i = 0
    new_path = path
    while os.path.isfile(new_path):
        i += 1
        new_path = add_suffix_to_path(
            path=path,
            suffix=f'_{i}'
        )

    return new_path


def get_tmp_filename(suffix: str = ".pdf", temp_dir: str = settings.TEMP_DIR, prefix: str = ''):
    """Create temporary file name

    Args:
        suffix (str, optional): File name suffix. Defaults to ".pdf".
        temp_dir (str, optional): Parent directory of created file. Defaults to settings.TEMP_DIR.
        prefix (str, optional): File name prefix. Defaults to ''.

    Returns:
        _type_: New temporary file name
    """
    with tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, dir=temp_dir) as fh:
        return fh.name


def read_json(path: str) -> dict:
    """Load dict from json file

    Args:
        path (str): Path to json file

    Returns:
        dict: Read dict
    """
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path: str, dictionary: dict) -> None:
    """Save dict as json file

    Args:
        path (str): Destination path
        dictionary (dict): Dictonary to be saved
    """
    with open(path, 'w') as f:
        json.dump(obj=dictionary, fp=f)
