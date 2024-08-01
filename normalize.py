import numpy as np
from datatypes import ArrayType, DataType


def normalize(source_arr: ArrayType, low: float, high: float) -> None:
    """
    Normalize the source array to values between `low` and `high` (ex: 0 and 256 for grayscale coloring)
    Normalizes the source array in place.
    """
    assert source_arr.dtype == DataType

    if high <= low:
        raise ValueError(
            "High value must be greater than low value in normalization.")

    arr_range = np.max(source_arr) - np.min(source_arr)
    new_range = high - low

    scale = new_range / arr_range
    source_arr *= scale
    # print('*=', scale)
    # print('=', source_arr)

    new_min = np.min(source_arr)
    offset = (low - new_min)
    source_arr += offset
    # print('+=', offset)
    # print('=', source_arr)
