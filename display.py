from PIL import Image, ImageDraw
from datatypes import ArrayType


def display(array: ArrayType):
    """Display a single array in an image, with a color scale gradient mapping to height."""
    size = max(1600 // (array.shape[0]-1), 1)

    img = Image.new(mode="RGB", size=(
        array.shape[0] * size, array.shape[1] * size), color=(255, 0, 0))

    draw = ImageDraw.Draw(img)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            value = int(array[i][j])
            if value < 100:
                color = (116, 204, 244)
            elif value < 120:
                color = (194, 178, 128)
            elif value < 180:
                color = (19, 109, 21)
            elif value < 240:
                color = (120, 120, 120)
            else:
                color = (235, 235, 235)
            draw.rectangle(
                ((i * size, j * size), (i * size + size, j * size + size)), fill=color, width=0)
            # draw.text((i * size, j * size),
            #           str(value), fill=(255, 0, 0))

    img.show()
