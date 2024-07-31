# use pillow or something idk idgaf
from PIL import Image, ImageDraw
import numpy as np
from numpy.typing import NDArray


def display(array: NDArray[np.float64]):
    size = max(1600 // (array.shape[0]-1), 1)

    img = Image.new(mode="RGB", size=(
        array.shape[0] * size, array.shape[1] * size), color=(255, 0, 0))

    draw = ImageDraw.Draw(img)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            value = int(array[i][j])
            if value < 0:
                color = (116, 204, 244)
            else:
                value += 100
                color = (value, value, value)
            draw.rectangle(
                ((i * size, j * size), (i * size + size, j * size + size)), fill=color, width=0)
            # draw.text((i * size, j * size),
            #           str(value), fill=(255, 0, 0))

    # img.save(r'C:\Users\ethan\code\terrain-gen\img.png')
    img.show()
