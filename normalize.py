import numpy as np
from datatypes import ArrayType, DataType


def normalize(source_arr: ArrayType, low: float, high: float) -> ArrayType:
    """
    Normalize the source array to values between `low` and `high` (ex: 0 and 256 for grayscale coloring).
    Returns the normalized array, which is of the same data type.
    """
    # assert source_arr.dtype == DataType

    if high <= low:
        raise ValueError(
            "High value must be greater than low value in normalization.")

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
    x = np.asarray([-256, 0, 256], dtype=np.float64)
    print('---', normalize(x, -512, 512))
    print('---', normalize(x, -16, 16))
