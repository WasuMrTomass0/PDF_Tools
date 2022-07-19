from multiprocessing.sharedctypes import Value
import tempfile
from PIL.Image import Image


def resize_image_fixed_scale(img, new_width, new_height):
    # Calculate scale
    scale_width = new_width / img.width
    scale_height = new_height / img.height
    if scale_width < scale_height:
        scale = scale_width
    else:
        scale = scale_height
    # Calculate new size
    new_width = int(img.width * scale)
    new_height = int(img.height * scale)
    # Resize
    if new_width > 0 and new_height > 0:
        img = img.resize((new_width, new_height))
    return img


def get_tmp_filename(suffix: str = ".pdf", temp_dir: str = 'data/work_dir/temp'):
    with tempfile.NamedTemporaryFile(suffix=suffix, dir=temp_dir) as fh:
        return fh.name


def rectangle_from_two_points(p1: "tuple[int, int]", p2: "tuple[int, int]", width: int, height: int) -> "tuple[float, float, float, float]":
    # Unpack
    x1, y1 = p1
    x2, y2 = p2
    # Find corners
    min_x = min(x1, x2)
    min_y = min(y1, y2)
    # Convert to 0.0-1.0
    return min_x / width, min_y / height, abs(x1 - x2) / width, abs(y1 - y2) / height    


def merge_images(bg_img: Image, fg_img: Image, pos: tuple) -> Image:
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

