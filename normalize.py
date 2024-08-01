import numpy as np
from datatypes import ArrayType, DataType


def normalize(source_arr: ArrayType, low: float, high: float) -> ArrayType:
    """
    Normalize an array to values between `low` and `high` (ex: 0 and 256 for grayscale coloring).
    Returns the normalized array, not modifying source array in place.
    Source array and resulting normalized array must be/are of type `ArrayType`.
    """
    if high <= low:
        raise ValueError(
            "High value must be greater than low value in normalization.")
    if source_arr.dtype != DataType:
        raise ValueError(f"Source array must be of type {DataType}.")

    arr_range = np.max(source_arr) - np.min(source_arr)
    # print(arr_range, np.max(source_arr), np.min(source_arr))
    new_range = high - low

    if arr_range == 0:
        raise ValueError(
            "Array must consist of two different values, not just one single value.")

    array = np.copy(source_arr)

    scale = new_range / arr_range
    array *= scale

    new_min = np.min(array)
    offset = low - new_min
    array += offset

    return array


if __name__ == '__main__':
    x = np.asarray([-256, 0, 256], dtype=DataType)
    print('---', normalize(x, -512, 512))
    print('---', normalize(x, -16, 16))
