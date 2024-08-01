
import typing
import numpy as np
import math
import random
from datatypes import DataType, Point, ArrayType

SMOOTHNESS = 0.55
AMPLITUDE = 100


def _get_value(array: ArrayType, point: Point) -> float | None:
    """Gets the array value at a point [x, y]. If the point is out of bounds of the array, return None."""
    if point.x < 0 or point.x > array.shape[0] - 1 or point.y < 0 or point.y > array.shape[0] - 1:
        return None
    return array[point.y, point.x]


def _find_avg(array: ArrayType, midpoint: Point, width: int, step: typing.Literal['diamond', 'square']) -> float:
    """Finds the average value of the points around point [x, y]. If the point is on the edge, then only take the average of the 3 existing points."""
    total = 0
    if step == 'diamond':
        # the points surrounding a point made in the diamond steps ALWAYS exist and are in the array
        for point in (
            Point(midpoint.x-width, midpoint.y+width),
            Point(midpoint.x+width, midpoint.y+width),
            Point(midpoint.x-width, midpoint.y-width),
            Point(midpoint.x+width, midpoint.y-width)
        ):
            total += _get_value(array, point)  # type: ignore
        return total / 4
    elif step == 'square':
        count = 4
        for point in (
            Point(midpoint.x, midpoint.y-width),
            Point(midpoint.x, midpoint.y+width),
            Point(midpoint.x-width, midpoint.y),
            Point(midpoint.x+width, midpoint.y)
        ):
            value = _get_value(array, point)
            if value is None:
                count -= 1
            else:
                total += value
        return total / count


def _diamonds_step(array: ArrayType, width: int, amplitude: float) -> None:
    """
    Rather than following the visualization steps found on the Wikipedia (https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Diamond_Square.svg/1920px-Diamond_Square.svg.png)
    Just calculate the start, stop, and step points for the diamond points.
    """
    size = array.shape[0]
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
            avg = _find_avg(array, Point(x, y),
                            half_width, step="diamond")
            randomness = random.uniform(-amplitude, amplitude)
            array[y, x] = avg + randomness


def _square_step(array: ArrayType, width: int, amplitude: float) -> None:
    """
    Rather than following the visualization steps found on the Wikipedia (https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Diamond_Square.svg/1920px-Diamond_Square.svg.png)
    Just calculate the start, stop, and step points for the square points.
    """
    size = array.shape[0]
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
            avg = _find_avg(array, Point(x, y),
                            half_width, step="square")
            randomness = random.uniform(-amplitude, amplitude)
            array[y, x] = avg + randomness
        alternate = not alternate


def _diamond_square(array: ArrayType, smoothness=SMOOTHNESS, amplitude=AMPLITUDE) -> ArrayType:
    """
    Runs the diamond square algorithm on the given (presumably seeded) array, in place.
    """
    shape = array.shape
    width = shape[0] - 1

    while width > 1:
        # perform diamond step
        _diamonds_step(array, width, amplitude)
        # perform square step
        _square_step(array, width, amplitude)

        width //= 2
        amplitude *= math.pow(2, -smoothness)

    return array


def generate(source_arr: ArrayType, smoothness=SMOOTHNESS, amplitude=AMPLITUDE) -> ArrayType:
    """
    Given a seeded `source_arr` of `ArrayType`, populate it with values using the diamond square algorithm, 
    described at https://en.wikipedia.org/wiki/Diamond-square_algorithm.

    Ensure that source array is of correct type (`DataType` and `ArrayType`) and is a square shape with a width of `2^n+1` for integer `n` > 0.

    Returns a new array, of type `ArrayType`, after which the diamond square algorithm has taken place (using the seeded values).
    """
    if source_arr.shape[0] != source_arr.shape[1] or not math.log2(source_arr.shape[0] - 1).is_integer() or not math.log2(source_arr.shape[1] - 1).is_integer():
        raise ValueError(
            "Souce array must be of a square shape, with a width of `2^n + 1`, where `n` is any positive integer.")
    if source_arr.dtype != DataType:
        raise ValueError(f"Source array must be of type {DataType}.")

    array = np.copy(source_arr)
    return _diamond_square(array, smoothness, amplitude)
