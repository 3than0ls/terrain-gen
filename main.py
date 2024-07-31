import numpy as np
from generator import diamond_square
from display import display

# https://en.wikipedia.org/wiki/Diamond-square_algorithm


# TODO: normalizing function to apply onto entire matrix so it all fits between 0 to 256
# TODO: njit optimization
# TODO: update README


def main():
    SFACTOR = 9
    size = 2 ** SFACTOR + 1
    nparray = np.zeros((size, size))

    diamond_square(nparray)

    display(nparray)


if __name__ == "__main__":
    main()
