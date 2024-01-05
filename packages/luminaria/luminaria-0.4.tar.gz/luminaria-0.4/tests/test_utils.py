import unittest
from luminaria.utils import map_value


class TestMapValueFunction(unittest.TestCase):
    def test_map_value(self):
        # Test case 1: Map 50 from range [0, 100] to [0, 1]
        result = map_value(50, 0, 100, 0, 1)
        self.assertAlmostEqual(result, 0.5, delta=0.001)

        # Test case 2: Map 75 from range [0, 100] to [0, 0.5]
        result = map_value(75, 0, 100, 0, 0.5)
        self.assertAlmostEqual(result, 0.375, delta=0.001)

        # Test case 3: Map 25 from range [0, 50] to [0, 1]
        result = map_value(25, 0, 50, 0, 1)
        self.assertAlmostEqual(result, 0.5, delta=0.001)

        # Test case 4: Map 0 from range [0, 1] to [0, 100]
        result = map_value(0, 0, 1, 0, 100)
        self.assertAlmostEqual(result, 0, delta=0.001)

        # Test case 5: Map 1 from range [0, 1] to [50, 100]
        result = map_value(1, 0, 1, 50, 100)
        self.assertAlmostEqual(result, 100, delta=0.001)


if __name__ == '__main__':
    unittest.main()