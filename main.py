import numpy as np
from generator import diamond_square
import random
from display import display

# https://en.wikipedia.org/wiki/Diamond-square_algorithm


def seed_value(rand: bool = True):
    if rand:
        return random.uniform(-256, 256)
    else:
        return 0


def main():
    SFACTOR = 9
    size = 2 ** SFACTOR + 1
    nparray = np.zeros((size, size))

    # nparray[0][0] = seed_value()
    # nparray[size-1][0] = seed_value()
    # nparray[0][size-1] = seed_value()
    # nparray[size-1][size-1] = seed_value()

    diamond_square(nparray)

    display(nparray)


if __name__ == "__main__":
    main()
