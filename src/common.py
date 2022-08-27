from PIL import Image
import tempfile
import json
import os

import settings


def init_check() -> None:
    """Checks done on initialise
    """
    create_directories()
    pass


def create_directories() -> None:
    """Create data structure
    """
    dirs = (
        settings.DATA_DIR,
        settings.POPPLER_DIR,
        settings.SIGNATURES_DIR,
        settings.INVALID_SIGNATURES_DIR,
        settings.TEMP_DIR,
        settings.LANGUAGES_DIR
    )

    for d in dirs:
        if not os.path.isdir(d):
            os.mkdir(d)
    pass


def get_new_dimensions_fixed_scale(old_dim: "tuple[int, int]", new_dim: "tuple[int, int]") -> "tuple[int, int]":
    """Calculate new dimension to be in fixed scale and not exceed rectangle

    Args:
        old_dim (tuple[int, int]): Old dimensions
        new_dim (tuple[int, int]): New dimension not in fixed scale

    Returns:
        tuple[int, int]: New dimension in fixed scale
    """
    old_width, old_height = old_dim
    new_width, new_height = new_dim
    # Calculate scale
    scale_width = new_width / old_width
    scale_height = new_height / old_height
    if scale_width < scale_height:
        scale = scale_width
    else:
        scale = scale_height
    # Calculate new size
    new_width = int(old_width * scale)
    new_height = int(old_height * scale)
    return new_width, new_height


def add_suffix_to_path(path: str, suffix: str) -> str:
    if '.' not in path:
        return path + suffix
    
    parts = path.split('.')
    extension = parts[-1]
    path = '.'.join(parts[:-1])
    return path + suffix + '.' + extension


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


def rectangle_from_two_points(p1: "tuple[int, int]", p2: "tuple[int, int]", width: int, height: int) -> "tuple[float, float, float, float]":
    """Create rectangle data from two (x,y) points

    Args:
        p1 (tuple[int, int]): First (x, y) point
        p2 (tuple[int, int]): Second (x, y) point
        width (int): Width used to scale to range [0.0-1.0]
        height (int): Width used to scale to range [0.0-1.0]

    Returns:
        tuple[float, float, float, float]: Rectangle tuple
    """
    # Unpack
    x1, y1 = p1
    x2, y2 = p2
    # Find corners
    min_x = min(x1, x2)
    min_y = min(y1, y2)
    # Convert to 0.0-1.0
    return min_x / width, min_y / height, abs(x1 - x2) / width, abs(y1 - y2) / height    


def read_json(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path: str, dictionary: dict) -> None:
    with open(path, 'w') as f:
        json.dump(obj=dictionary, fp=f)
