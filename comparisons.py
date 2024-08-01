from PIL import Image, ImageDraw, ImageFont
import numpy as np
from generate import generate, normalize
from generate.typing import ArrayType


def draw_single(draw: ImageDraw.ImageDraw, array: ArrayType, display_size: int, offset: tuple[int, int]):
    """
    Draws a single map array matrix on the larger ImageDraw canvas, given the display size and the offset (position of map)
    """
    unit_size = max(display_size // (array.shape[0]-1), 1)

    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            value = int(array[x, y])
            color = (value, value, value)

            draw.rectangle(
                xy=((offset[0] + x * unit_size, offset[1] + y * unit_size),
                    (offset[0] + x * unit_size + unit_size,
                     offset[1] + y * unit_size + unit_size)),
                fill=color,
                width=0
            )


def comparisons(map_size_factor=7, s_range=[x / 10.0 for x in range(0, 13)], amp_range=range(50, 650, 100)):
    """
    Compares maps for ranges of terrain smoothness (`s_range`) and amplitude (`amp_range`) in a single PNG.
    """
    UNIT_SIZE = 4  # size of an individual pixel/value in each array

    map_size = 2 ** map_size_factor + 1

    display_size = map_size * UNIT_SIZE
    border_size = UNIT_SIZE * 5

    dims = (len(s_range) * (display_size + border_size) + border_size,
            len(amp_range) * (display_size + border_size) + border_size)
    img = Image.new(mode="RGB", size=dims, color=(255, 0, 0))
    draw = ImageDraw.Draw(img)

    seed = np.zeros((map_size, map_size), dtype=np.float32)

    for s_i, smoothness in enumerate(s_range):
        for amp_i, amplitude in enumerate(amp_range):
            offset = (border_size + s_i * (display_size + border_size),
                      border_size + amp_i * (display_size + border_size))

            result = generate(seed, smoothness, amplitude)
            normalized = normalize(result, 0, 256)
            draw_single(draw, normalized, display_size, offset)

            font = ImageFont.truetype("arial.ttf", 25)
            draw.text(
                xy=(offset[0]+UNIT_SIZE,
                    offset[1]+UNIT_SIZE),
                text=f"Smoothness: {smoothness}\nAmplitude: {
                    amplitude}\nNormalized: 0-256",
                fill=(255, 0, 0),
                font=font
            )

    img.show("DS Smoothness and Amplitude Comparisons (Normalized 0-256)")
    # img.save("./comparisons.png")


if __name__ == '__main__':
    # comparisons(map_size_factor=7, s_range=[0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4,
    #             5, 10, 15, 20, 50, 100, 1000, 10000, 100000], amp_range=range(50, 250, 50))
    comparisons()
