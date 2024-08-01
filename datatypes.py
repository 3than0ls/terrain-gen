from numpy.typing import NDArray
import numpy as np
from dataclasses import dataclass

DataType = np.float64
ArrayType = NDArray[DataType]


@dataclass
class Point:
    x: int
    y: int
