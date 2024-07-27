import numpy as np
from generator import diamond_square
import random
from display import display

# https://en.wikipedia.org/wiki/Diamond-square_algorithm


def main():
    source = [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
    ]

    nparray = np.asarray(source, np.float64)
    SFACTOR = 8
    size = 2 ** SFACTOR + 1
    nparray = np.zeros((size, size))
    nparray[0][0] = random.random()
    nparray[0][size-1] = random.random()
    nparray[size-1][0] = random.random()
    nparray[size-1][size-1] = random.random()
    # arr = np.zeros((31, 31), dtype=np.float64)
    # arr = np.ndarray()
    diamond_square(nparray)
    print(nparray)

    display(nparray)


if __name__ == "__main__":
    main()
