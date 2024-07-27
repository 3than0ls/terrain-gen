from re import L
import numpy as np
import math
import statistics
import random
from numpy.typing import NDArray
from datatypes import Point, Square, Diamond

SCALE_CONST = 1
TERRAIN_SMOOTHNESS = 0.5


def _get_point_value(source_arr: NDArray[np.float64], point: Point) -> float:
    """Gets the array value at a point. If the point is out of bounds of the array, return -1."""
    if point.x < 0 or point.x > source_arr.shape[0] - 1 or point.y < 0 or point.y > source_arr.shape[0] - 1:
        return -1
    return source_arr[point.y][point.x]


def _find_average(source_arr: NDArray[np.float64], shape: Square | Diamond) -> float:
    """Find the average value of the surrounding points of a Square or Diamond.
    Square average is computed during diamond steps, and thus all points always exist
    Diamond average is computed during square step, and some points may not be in bounds of the source array.
    """
    if isinstance(shape, Square):
        # computed during diamond step
        total = sum((_get_point_value(source_arr, point) for point in (
            shape.top_left, shape.top_right, shape.bottom_left, shape.bottom_right)))
    elif isinstance(shape, Diamond):
        # computed during square step
        # incorrect implementation, doesnt use average of surrounding points instead just uses 0
        total = 0
        points = [shape.top, shape.left, shape.right, shape.bottom]
        for point in points:
            if _get_point_value(source_arr, point) == -1:
                total += sum([_get_point_value(source_arr, p)
                              for p in points if p != point]) / 3
            else:
                total += _get_point_value(source_arr, point)

    avg = total / 4
    avg = round(avg, 2)
    return avg


def random_value(iteration: int) -> float:
    return random.random() * SCALE_CONST * math.pow(TERRAIN_SMOOTHNESS, iteration)


def generate_diamonds_from_window(window: Square) -> tuple[Diamond, Diamond, Diamond, Diamond]:
    # top diamond, left diamond, right diamond, bottom diamond
    return (
        Diamond(Point(window.midpoint.x, window.midpoint.y -
                window.size // 2), window.size // 2),
        Diamond(Point(window.midpoint.x - window.size //
                2, window.midpoint.y), window.size // 2),
        Diamond(Point(window.midpoint.x + window.size //
                2, window.midpoint.y), window.size // 2),
        Diamond(Point(window.midpoint.x, window.midpoint.y +
                window.size // 2), window.size // 2),
    )


def _diamond_step(source_arr: NDArray[np.float64], window: Square, iteration: int) -> tuple[Diamond, Diamond, Diamond, Diamond]:
    midpoint = window.midpoint
    value = _find_average(source_arr, window)
    source_arr[midpoint.y][midpoint.x] = value + random_value(iteration)
    return generate_diamonds_from_window(window)


def generate_squares_from_window(window: Square) -> tuple[Square, Square, Square, Square]:
    new_size = (window.size) // 2
    return (
        Square(window.top_left, new_size),
        Square(Point(window.top_left.x + window.size //
               2, window.top_left.y), new_size),
        Square(Point(window.top_left.x, window.top_left.y +
               new_size), new_size),
        Square(Point(window.top_left.x + window.size //
               2, window.top_left.y + new_size), new_size),
    )


def _square_step(source_arr:  NDArray[np.float64], window: Square, diamonds: tuple[Diamond, Diamond, Diamond, Diamond], iteration: int) -> tuple[Square, Square, Square, Square]:
    for diamond in diamonds:
        midpoint = diamond.midpoint
        value = _find_average(source_arr, diamond)
        source_arr[midpoint.y][midpoint.x] = value + random_value(iteration)

    return generate_squares_from_window(window)


def _square_out_of_bounds(source_arr: NDArray[np.float64], square: Square) -> bool:
    return square.top_left.x < 0 or square.top_left.y < 0 or square.bottom_right.x > source_arr.shape[0]-1 or square.bottom_right.y > source_arr.shape[0]


def diamond_square(source_arr: NDArray[np.float64], window: Square | None = None, iteration=1) -> tuple[Square, Square, Square, Square] | None:
    assert source_arr.shape[0] == source_arr.shape[1]
    assert math.log2(source_arr.shape[0] - 1).is_integer()
    assert math.log2(source_arr.shape[1] - 1).is_integer()

    if window is not None and (window.size <= 1 or _square_out_of_bounds(source_arr, window)):
        return

    if window is None:
        window = Square(Point(0, 0), source_arr.shape[0]-1)

    diamonds = _diamond_step(source_arr, window, iteration)
    squares = _square_step(source_arr, window, diamonds, iteration)

    for square in squares:
        diamond_square(source_arr, square, iteration + 1)
