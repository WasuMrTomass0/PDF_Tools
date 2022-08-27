from PIL import Image
import common


def remove_background(
        img: Image.Image,
        r_range: "tuple[int, int]",
        g_range: "tuple[int, int]",
        b_range: "tuple[int, int]"
    ) -> Image:
    # Convert to RGBA
    img = img.convert("RGBA")
    data = img.getdata()
    # Check if value is in range
    def in_range(v: int, v_range: "tuple[int, int]") -> bool:
        return v_range[0] <= v <= v_range[1]
    # Iterate through all pixels and make transparent if it is given range
    new_data = []
    for r, g, b, a in data:
        if in_range(r, r_range) and in_range(g, g_range) and in_range(b, b_range):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((r, g, b, a))
    # Save as image
    img.putdata(new_data)
    return img


def resize_image_fixed_scale(img, new_width: int, new_height: int):
    """Resize image in fixed scale ratio

    Args:
        img (_type_): Input image
        new_width (int): New width
        new_height (int): New height

    Returns:
        _type_: Resized image
    """
    new_width, new_height = common.get_new_dimensions_fixed_scale(
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
