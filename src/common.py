

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
