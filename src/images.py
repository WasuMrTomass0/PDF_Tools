from PIL import Image


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
