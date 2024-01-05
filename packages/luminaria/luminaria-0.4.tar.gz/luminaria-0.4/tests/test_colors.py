import unittest
from luminaria.colors import same, add, blend, fade, BLACK, RED, GREEN


class TestSameFunction(unittest.TestCase):

    def test_same_identical_colors(self):
        color1 = RED
        color2 = RED

        # Assert that identical colors are considered the same
        result = same(color1, color2)
        self.assertTrue(result)

    def test_same_similar_colors(self):
        color1 = RED
        color2 = (254.9991, 0.0009, 0)

        # Assert that slightly different colors within the default delta are considered the same
        result = same(color1, color2)
        self.assertTrue(result)

    def test_same_different_colors_outside_delta(self):
        color1 = RED
        color2 = (254.89, 0.11, 0)

        # Assert that different delta values affect the comparison
        result_default_delta = same(color1, color2)
        result_custom_delta = same(color1, color2, allowed_delta=0.2)

        self.assertFalse(result_default_delta)
        self.assertTrue(result_custom_delta)

    def test_same_invalid_colors(self):
        with self.assertRaises(ValueError):
            same((0.0, 0.0), BLACK)


class TestBlendFunction(unittest.TestCase):

    def test_blend_colors(self):
        # Test case 1
        result = blend(RED, GREEN, 0.5)
        self.assertEqual(result, (127.5, 127.5, 0))

        # Test case 2
        result = blend((255, 0, 0), (0, 0, 255), 0.25)
        self.assertEqual(result, (191.25, 0.0, 63.75))

        # Test case 3
        # result = blend(RED, YELLOW, 0.5)
        # self.assertEqual(result, (255.0, 127.5, 0.0))

    def test_invalid_input(self):
        # Test case for invalid input
        with self.assertRaises(ValueError):
            result = blend((255, 0, 0), (0, 255, 0, 255), 0.5)


class TestFadeFunction(unittest.TestCase):

    def test_fade_color(self):
        # Test case 1
        result = fade((255, 0, 0), 0.5)
        self.assertEqual(result, (127.5, 0, 0))

        # Test case 2
        result = fade((0, 255, 0), 0.25)
        self.assertEqual(result, (0, 63.75, 0))

    def test_fade_to_black(self):
        # Test case for fading to black
        result = fade((100, 150, 200), 0.0)
        self.assertEqual(result, BLACK)  # Fading with ratio 0.0 should result in black

    def test_invalid_input(self):
        # Test case for invalid input
        with self.assertRaises(ValueError):
            fade((255, 0, 0, 255), 0.5)

        with self.assertRaises(ValueError):
            fade(BLACK, -0.1)

        with self.assertRaises(ValueError):
            fade(BLACK, 1.1)


class TestAddFunction(unittest.TestCase):
    def test_adding_colors(self):
        # Test case 1
        result = add((100, 50, 25), (50, 75, 30))
        self.assertEqual(result, (150, 125, 55))

        # Test case 2
        result = add((200, 100, 50), (30, 40, 60))
        self.assertEqual(result, (230, 140, 110))

        # Test case 3
        result = add((255, 255, 255), (0, 0, 0))
        self.assertEqual(result, (255, 255, 255))

    def test_color_constraining(self):
        # Test case 1
        result = add((200, 150, 100), (100, 150, 200))
        self.assertEqual(result, (255, 255, 255))  # All components should be constrained to 255

        # Test case 2
        result = add((300, 0, 0), (0, 0, 300))
        self.assertEqual(result, (255, 0, 255))  # Red and blue components should be constrained to 255

    def test_empty_input(self):
        # Test case for an empty input
        result = add()
        self.assertEqual(result, (0, 0, 0))  # Sum of an empty list should be (0, 0, 0)

    def test_invalid_color(self):
        with self.assertRaises(ValueError):
            add((0.0, 0.0))


if __name__ == '__main__':
    unittest.main()
