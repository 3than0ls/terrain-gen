import unittest
import numpy as np
from generator import diamond_square


class DiamondSquareTest(unittest.TestCase):
    def test_invalidsize(self):
        size = 2 ** 8 + 1
        invalid = np.zeros((size, size))
        with self.assertRaises(AssertionError):
            diamond_square(invalid)

        invalid = np.zeros((size, 10))

        with self.assertRaises(AssertionError):
            diamond_square(invalid)


if __name__ == '__main__':
    unittest.main()
