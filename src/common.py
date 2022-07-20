from PIL import Image
import tempfile
import os

import settings


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


def resize_image(img, new_width, new_height):
    # Resize
    if new_width > 0 and new_height > 0:
        img = img.resize((new_width, new_height))
    return img


def load_signature_image(signature_data: "list[list]", width: int, height: int) -> Image.Image:
    sign_path, resize_format, _, _, w, h = signature_data
    # Load signature
    with Image.open(sign_path) as signature_img:
        # Resize signature
        resize_function = resize_image_fixed_scale if resize_format else resize_image
        signature_img = resize_function(
            img=signature_img,
            new_width=int(w * width),
            new_height=int(h * height)
        )
        return signature_img



def get_tmp_filename(suffix: str = ".pdf", temp_dir: str = settings.TEMP_DIR, prefix: str = ''):
    with tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, dir=temp_dir) as fh:
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


def merge_images(bg_img: Image.Image, fg_img: Image.Image, pos: tuple) -> Image.Image:
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

