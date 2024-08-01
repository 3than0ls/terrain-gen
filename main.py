from pathlib import Path
import numpy as np
from generate import generate, normalize, DataType
from display import display, load_gradient

# https://en.wikipedia.org/wiki/Diamond-square_algorithm


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

    gradient = load_gradient(Path("./display/gradient.json"))
    display(normalized, gradient)


if __name__ == "__main__":
    main()
