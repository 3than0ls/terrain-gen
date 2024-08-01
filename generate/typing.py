from numpy.typing import NDArray
import numpy as np
from dataclasses import dataclass

DataType = np.float32
ArrayType = NDArray[DataType]


@dataclass
class Point:
    # for future note: dataclasses don't work with numba JIT
    x: int
    y: int
