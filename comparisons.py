from PIL import Image, ImageDraw, ImageFont
import numpy as np
from numpy.typing import NDArray

from generator import diamond_square
from normalize import normalize


def draw_single(draw: ImageDraw.ImageDraw, array: NDArray[np.float64], display_size: int, offset: tuple[int, int]):
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


def comparisons(map_size_factor=7, ts_range=[x / 10.0 for x in range(0, 11)], amp_range=range(50, 600, 50)):
    """
    Compares maps for ranges of terrain smoothness (`ts_range`) and amplitude (`amp_range`) in a single PNG.
    """
    UNIT_SIZE = 8  # size of an individual pixel/value in each array

    map_size = 2 ** map_size_factor + 1

    display_size = map_size * UNIT_SIZE
    border_size = UNIT_SIZE * 5

    dims = (len(ts_range) * (display_size + border_size) + border_size,
            len(amp_range) * (display_size + border_size) + border_size)
    img = Image.new(mode="RGB", size=dims, color=(255, 0, 0))
    draw = ImageDraw.Draw(img)

    # for terrain smoothness 0 to 1, step by 0.1
    for ts_i, terrain_smoothness in enumerate(ts_range):
        for amp_i, amplitude in enumerate(amp_range):
            seed = np.zeros((map_size, map_size))
            diamond_square(seed, terrain_smoothness, amplitude)
            normalize(seed, 0, 256)

            offset = (border_size + ts_i * (display_size + border_size),
                      border_size + amp_i * (display_size + border_size))
            draw_single(draw, seed, display_size, offset)

            font = ImageFont.truetype("arial.ttf", 25)
            draw.text(
                xy=(offset[0]+UNIT_SIZE,
                    offset[1]+UNIT_SIZE),
                text=f"Terrain Smoothness: {
                    terrain_smoothness}\nAmplitude: {amplitude}",
                fill=(255, 0, 0),
                font=font
            )

    img.show("DS Terrain Smoothness and Amplitude Comparisons (Normalized 0-256)")


if __name__ == '__main__':
    comparisons()
