from PIL import Image, ImageDraw
from generate.typing import ArrayType
from display.gradient import Gradient, get_color


def display(array: ArrayType, gradient: Gradient):
    """Display a single array in an image, with a color scale gradient mapping to height."""
    size = max(1600 // (array.shape[0]-1), 1)

    img = Image.new(mode="RGB", size=(
        array.shape[0] * size, array.shape[1] * size), color=(255, 0, 0))

    draw = ImageDraw.Draw(img)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            value = int(array[i][j])

            color = get_color(gradient, value)

            draw.rectangle(
                ((i * size, j * size), (i * size + size, j * size + size)), fill=color, width=0)
            # draw.text((i * size, j * size),
            #           str(value), fill=(255, 0, 0))

    img.show()
