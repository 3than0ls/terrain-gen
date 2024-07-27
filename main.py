import numpy as np
from generator import diamond_square
import random
from display import display

# https://en.wikipedia.org/wiki/Diamond-square_algorithm


def seed_value(rand: bool = False):
    if rand:
        return random.random()
    else:
        return 256/2


def main():
    SFACTOR = 5
    size = 2 ** SFACTOR + 1
    nparray = np.zeros((size, size))
    nparray[0][0] = seed_value()
    nparray[0][size-1] = seed_value()
    nparray[size-1][0] = seed_value()
    nparray[size-1][size-1] = seed_value()
    # arr = np.zeros((31, 31), dtype=np.float64)
    # arr = np.ndarray()
    diamond_square(nparray)
    print(nparray)

    display(nparray)


if __name__ == "__main__":
    main()
