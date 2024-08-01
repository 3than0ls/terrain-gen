from pathlib import Path
import numpy as np
from datatypes import DataType
from display.gradient import process_gradient
from generator import generate
from display.display import display
from normalize import normalize

# https://en.wikipedia.org/wiki/Diamond-square_algorithm


# DONE: normalizing function to apply onto entire matrix so it all fits between 0 to 256
# TODO: color range mapping
# TODO: update README

# TODO: post generation changes
#       - for every pixel; if the 4 directly adjacent pixels are of a certain value, set to those values
# TODO: 3 dimensional implementation

def main():
    size = 9
    arr_size = 2 ** size + 1
    seed = np.zeros((arr_size, arr_size), dtype=DataType)
    out = generate(seed)
    normalized = normalize(out, 0, 256)

    gradient = process_gradient(Path("./display/gradient.json"))
    display(normalized, gradient)


if __name__ == "__main__":
    main()
