import numpy as np
from generator import diamond_square
from display import display
from normalize import normalize

# https://en.wikipedia.org/wiki/Diamond-square_algorithm


# DONE: normalizing function to apply onto entire matrix so it all fits between 0 to 256
# TODO: color range mapping
# TODO: njit optimization
# TODO: type annotating and standards (Point, MapArray)
# TODO: update README


def main():
    size = 9
    arr_size = 2 ** size + 1
    seed = np.zeros((arr_size, arr_size))

    out = diamond_square(seed)
    normalized = normalize(out, 0, 256)
    display(normalized)


if __name__ == "__main__":
    main()
