# use pillow or something idk idgaf
from PIL import Image, ImageDraw
import numpy as np
from numpy.typing import NDArray
import math


def display(array: NDArray[np.float64]):
    size = 1000 // (array.shape[0])

    img = Image.new(mode="RGB", size=(
        array.shape[0] * size, array.shape[1] * size), color=(255, 0, 0))

    draw = ImageDraw.Draw(img)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            color = (int(array[i][j] * 256), int(array[i]
                     [j] * 256), int(array[i][j] * 256))
            draw.rectangle(
                ((i * size, j * size), (i * size + size, j * size + size)), fill=color, width=0)

    img.show()
