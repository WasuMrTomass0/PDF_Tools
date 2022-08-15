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


def resize_image_fixed_scale(img, new_width: int, new_height: int):
    """Resize image in fixed scale ratio

    Args:
        img (_type_): Input image
        new_width (int): New width
        new_height (int): New height

    Returns:
        _type_: Resized image
    """
    new_width, new_height = get_new_dimensions_fixed_scale(
        old_dim=(img.width, img.height),
        new_dim=(new_width, new_height)
     )
    # Resize
    if new_width > 0 and new_height > 0:
        img = img.resize((new_width, new_height))
    return img


def resize_image(img, new_width: int, new_height: int):
    """Resize image

    Args:
        img (_type_): Input image
        new_width (int): New width 
        new_height (int): New height 

    Returns:
        _type_: Resized image
    """
    if new_width > 0 and new_height > 0:
        img = img.resize((new_width, new_height))
    return img


def load_signature_image(signature_data: "list[list]", width: int = None, height: int = None) -> Image.Image:
    """Load signature image and resize it

    Args:
        signature_data (list[list]): Signature data 
        width (int): New width
        height (int): New height

    Returns:
        Image.Image: _description_
    """
    sign_path, resize_format, _, _, w, h = signature_data
    # Load signature
    signature_img = Image.open(sign_path).copy()
    if width and height:
        # Resize signature if dimensions were given
        resize_function = resize_image_fixed_scale if resize_format else resize_image
        signature_img = resize_function(
            img=signature_img,
            new_width=int(w * width),
            new_height=int(h * height)
        )
    return signature_img


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


def merge_images(bg_img: Image.Image, fg_img: Image.Image, pos: tuple) -> Image.Image:
    """Merge two images

    Args:
        bg_img (Image.Image): Background image
        fg_img (Image.Image): Foreground image
        pos (tuple): Position of foreground image

    Raises:
        ValueError: Invalid position
        ValueError: Invalid type of elements in pos

    Returns:
        Image.Image: _description_
    """
    # Convert position
    if len(pos) != 2:
        raise ValueError(f'Position is invalid. Expected (x, y). Got {pos}')
    x, y = pos
    if type(x) is int and type(y) is int:
        pass
    elif type(x) is float and type(y) is float:
        x = int(x * bg_img.width)
        y = int(y * bg_img.height)
    else:
        raise ValueError(f'Position is invalid type. Expected int or float. Got {type(x), type(y)}')
    # Merge images
    bg_img.paste(fg_img, (x, y), fg_img.convert('RGBA'))

    return bg_img


def read_json(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path: str, dictionary: dict) -> None:
    with open(path, 'w') as f:
        json.dump(obj=dictionary, fp=f)
