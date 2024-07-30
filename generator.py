
import typing
import numpy as np
import math
import random
from numpy.typing import NDArray
from datatypes import Point

ArrayType = NDArray[np.float64]


TERRAIN_SMOOTHNESS = 0.55
SCALE_CONST = 100


# BIND = True
# BIND_MIN = -256
# BIND_MAX = 256

# def _bind(value: float | int, minimum=BIND_MIN, maximum=BIND_MAX):
#     return min(max(value, minimum), maximum) if BIND else value


def _random_value(iteration: int) -> float:
    scale = SCALE_CONST
    shrink_factor = math.pow(math.pow(2, -TERRAIN_SMOOTHNESS), iteration)
    # shrink_factor = 1
    return random.uniform(-scale * shrink_factor, scale * shrink_factor)


def _get_value(source_arr: NDArray[np.float64], point: Point) -> float | None:
    """Gets the array value at a point [x, y]. If the point is out of bounds of the array, return None."""
    if point.x < 0 or point.x > source_arr.shape[0] - 1 or point.y < 0 or point.y > source_arr.shape[0] - 1:
        return None
    return source_arr[point.y, point.x]


def _find_avg(source_arr: NDArray[np.float64], midpoint: Point, width: int, step: typing.Literal['diamond', 'square']) -> float:  # type: ignore
    """Finds the average value of the points around point [x, y]. If the point is on the edge, then only take the average of the 3 existing points."""
    size = source_arr.shape[0]
    total = 0
    if step == 'diamond':
        # the points surrounding a point made in the diamond steps ALWAYS exist and are in the array
        for point in (
            Point(midpoint.x-width, midpoint.y+width),
            Point(midpoint.x+width, midpoint.y+width),
            Point(midpoint.x-width, midpoint.y-width),
            Point(midpoint.x+width, midpoint.y-width)
        ):
            total += _get_value(source_arr, point)  # type: ignore
        return total / 4
    elif step == 'square':
        count = 4
        for point in (
            Point(midpoint.x, midpoint.y-width),
            Point(midpoint.x, midpoint.y+width),
            Point(midpoint.x-width, midpoint.y),
            Point(midpoint.x+width, midpoint.y)
        ):
            value = _get_value(source_arr, point)
            if value is None:
                count -= 1
            else:
                total += value
        return total / count


def diamond_step(source_arr: ArrayType, width: int, iteration: int) -> None:
    """
    Rather than following the visualization steps found on the Wikipedia (https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Diamond_Square.svg/1920px-Diamond_Square.svg.png)
    Just calculate the start, stop, and step points for the diamond points.
    """
    size = source_arr.shape[0]
    half_width = width // 2
    params = (half_width, size, width)

    """
    Iteration params:
    start   half_width      diamond generation always starts at a half width (the offset which finds the midpoints of every square)
    stop    size            diamond generation always ends before the end of the array, but we leave stop as size because step will take care of this stop-before-array-end process
    step    width * 2       diamond generation finds midpoints of squares, which can be found by half_width + (width), ensuring you don't get the edges of squares, only midpoints
    """
    for y in range(*params):
        for x in range(*params):
            avg = _find_avg(source_arr, Point(x, y),
                            half_width, step="diamond")
            randomness = _random_value(iteration)
            source_arr[y, x] = avg + randomness


def square_step(source_arr: ArrayType, width: int, iteration: int) -> None:
    """
    Rather than following the visualization steps found on the Wikipedia (https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Diamond_Square.svg/1920px-Diamond_Square.svg.png)
    Just calculate the start, stop, and step points for the square points.
    """
    size = source_arr.shape[0]
    half_width = width // 2
    alternate = True

    """
    Y-iteration params:
    start   0           square point generation has a minimum of zero (there will always be points generated at 0)
    stop    size        square point generation has a maximum of size (there will always be points generated up to the end [size-1, range stop not included])
    step    half_width  square point generation step half widths downwards.
    """
    for y in range(0, size, half_width):
        """
        X-iteration params:
        start   half_width * int(alternate)     the only real thing to note; the start of x alternates between a step and no step as you go down
        stop    size                            square point generation has a maximum of size (there will always be points generated up to the end [size-1, range stop not included])
        step    half_width                      square point generation steps full widths across
        """
        for x in range(half_width * int(alternate), size, width):
            avg = _find_avg(source_arr, Point(x, y),
                            half_width, step="square")
            randomness = _random_value(iteration)
            source_arr[y, x] = avg + randomness
        alternate = not alternate


def diamond_square(source_arr: ArrayType, window=None) -> ArrayType:
    assert source_arr.shape[0] == source_arr.shape[1]
    assert math.log2(source_arr.shape[0] - 1).is_integer()
    assert math.log2(source_arr.shape[1] - 1).is_integer()

    shape = source_arr.shape

    width = shape[0] - 1
    iteration = 0

    while width > 1:
        midpoint = source_arr.shape

        # perform diamond step
        diamond_step(source_arr, width, iteration)
        # perform square step
        square_step(source_arr, width, iteration)

        width //= 2
        iteration += 1

    return source_arr
