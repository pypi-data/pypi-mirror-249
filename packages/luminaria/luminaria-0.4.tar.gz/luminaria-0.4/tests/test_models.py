import unittest
from unittest.mock import patch

from luminaria.models import Solid, Gradient, MultiGradient, Map, Triangle, Reverse, Add, Window, Flame
from luminaria import colors


class TestSolidModel(unittest.TestCase):
    def test_render(self):
        # Create an instance of Solid with a specific color
        solid_model = Solid("TestSolid", (100, 50, 25))

        # Test the render method
        result = solid_model.render(0.5)
        expected_result = (100, 50, 25)
        self.assertEqual(result, expected_result)


class TestGradientModel(unittest.TestCase):
    def test_render(self):
        # Create an instance of Gradient with different colors
        gradient_model = Gradient("TestGradient", (100, 200, 50), (50, 100, 200))

        # Test the render method with different positions
        result_pos_0 = gradient_model.render(0.0)
        result_pos_0_5 = gradient_model.render(0.5)
        result_pos_1 = gradient_model.render(1.0)

        # Expected results based on the provided colors
        expected_pos_0 = (100, 200, 50)  # Color at position 0 should be the first color (c1)
        expected_pos_0_5 = (75, 150, 125)  # Middle point between c1 and c2
        expected_pos_1 = (50, 100, 200)  # Color at position 1 should be the second color (c2)

        # Check the results
        self.assertEqual(result_pos_0, expected_pos_0)
        self.assertEqual(result_pos_0_5, expected_pos_0_5)
        self.assertEqual(result_pos_1, expected_pos_1)


class TestMultiGradientModel(unittest.TestCase):

    def test_render(self):
        # Create an instance of MultiGradient with different colors
        multi_gradient_model = MultiGradient("TestMultiGradient", [(255, 0, 0), (0, 255, 0), (0, 0, 255)])

        # Test the render method with different positions
        result_pos_0 = multi_gradient_model.render(0.0)
        result_pos_0_25 = multi_gradient_model.render(0.25)
        result_pos_0_5 = multi_gradient_model.render(0.5)
        result_pos_0_75 = multi_gradient_model.render(0.75)
        result_pos_1 = multi_gradient_model.render(1.0)

        # Expected results based on the provided colors
        expected_pos_0 = (255, 0, 0)  # Color at position 0 should be the first color in the list
        expected_pos_0_25 = (127.5, 127.5, 0)  # Quarter point between c1 and c2
        expected_pos_0_5 = (0, 255, 0)  # Middle point between the first and second colors
        expected_pos_0_75 = (0, 127.5, 127.5)  # Three-quarter point between c2 and c3
        expected_pos_1 = (0, 0, 255)  # Color at position 1 should be the last color in the list

        # Check the results
        self.assertEqual(result_pos_0, expected_pos_0)
        self.assertEqual(result_pos_0_25, expected_pos_0_25)
        self.assertEqual(result_pos_0_5, expected_pos_0_5)
        self.assertEqual(result_pos_0_75, expected_pos_0_75)
        self.assertEqual(result_pos_1, expected_pos_1)

    def test_render_edge_cases(self):
        # Test edge cases when position is at the boundaries
        multi_gradient_model = MultiGradient("TestMultiGradient", [colors.RED, colors.GREEN, colors.BLUE])

        # Position at the beginning (0.0)
        result_pos_0 = multi_gradient_model.render(0.0)
        self.assertEqual(result_pos_0, (255, 0, 0))

        # Position in the middle (0.5)
        result_pos_0_5 = multi_gradient_model.render(0.5)
        self.assertEqual(result_pos_0_5, (0, 255, 0))

        # Position at the end (1.0)
        result_pos_1 = multi_gradient_model.render(1.0)
        self.assertEqual(result_pos_1, (0, 0, 255))


class TestMapModel(unittest.TestCase):
    def test_render(self):
        # Create an instance of Map with a Gradient model (RED -> GREEN)
        gradient_model = Gradient("TestGradient", colors.RED, colors.GREEN)
        map_model = Map("TestMap", 0.0, 0.5, 0.4, 0.9, gradient_model)

        # Test the render method with positions inside the mapped range
        pos_values = [0.3, 0.4, 0.5, 0.9, 0.95]
        expected_results = [
            colors.BLACK,  # outside of range
            colors.RED,
            colors.blend(colors.RED, colors.GREEN, 0.1),
            colors.blend(colors.RED, colors.GREEN, 0.5),
            colors.BLACK  # outside of range
        ]

        for pos, expected_result in zip(pos_values, expected_results):
            with self.subTest(pos=pos):
                result = map_model.render(pos)
                self.assertTrue(colors.same(result, expected_result), f"{result} != {expected_result}")


class TestTriangle(unittest.TestCase):

    def test_render_inside_range(self):
        triangle_model = Triangle("TestTriangle", 0.3, 0.7, colors.RED)

        # Test rendering at various positions within the range
        result_color_rising = triangle_model.render(0.4)
        result_color_midpoint = triangle_model.render(0.5)
        result_color_falling = triangle_model.render(0.65)

        expected_result_color_rising = colors.fade(colors.RED, 0.5)
        expected_result_color_midpoint = colors.RED
        expected_result_color_falling = colors.fade(colors.RED, 0.25)

        # Assert that the colors are as expected
        self.assertTrue(colors.same(result_color_rising, expected_result_color_rising),
                        f"{result_color_rising} != {expected_result_color_rising}")
        self.assertTrue(colors.same(result_color_midpoint, expected_result_color_midpoint),
                        f"{result_color_midpoint} != {expected_result_color_midpoint}")
        self.assertTrue(colors.same(result_color_falling, expected_result_color_falling),
                        f"{result_color_falling} != {expected_result_color_falling}")

    def test_render_outside_range(self):
        triangle_model = Triangle("TestTriangle", 0.2, 0.8, colors.RED)

        # Test rendering outside the specified range
        result_color_before_range = triangle_model.render(0.1)
        result_color_after_range = triangle_model.render(0.9)

        # Assert that colors are black
        self.assertEqual(result_color_before_range, colors.BLACK)
        self.assertEqual(result_color_after_range, colors.BLACK)


class TestReverseClass(unittest.TestCase):

    def test_reverse_rendering(self):
        # Create an original gradient model
        original_model = Gradient("OriginalGradient", colors.RED, colors.GREEN)

        # Create a reversed model
        reversed_model = Reverse("ReversedGradient", original_model)

        # Render the reversed model at a specific position
        result_color = reversed_model.render(0.75)

        # Expected result_color is the reverse of the color at 0.75 in the original model
        expected_color = original_model.render(1.0 - 0.75)

        # Assert that the result_color matches the expected_color
        self.assertEqual(result_color, expected_color)


class TestAddModel(unittest.TestCase):
    def test_render(self):
        # Create instances of MockModel with specific colors
        model1 = Solid("model1", (100, 50, 25))
        model2 = Solid("model2", (50, 75, 30))
        model3 = Solid("model3", (200, 100, 50))

        # Create an instance of Add with the mock models
        add_model = Add("TestAdd", [model1, model2, model3])

        # Test the render method
        result = add_model.render(0.5)
        expected_result = (255, 225, 105)
        self.assertEqual(result, expected_result)


class TestWindow(unittest.TestCase):
    def test_render(self):
        # Create models for inside and outside the window
        inside_model = Solid("inside-red", colors.RED)
        outside_model = Solid("outside-blue", colors.BLUE)

        # Create a window that transitions from the inside model to the outside model
        window_model = Window("TestWindow", 0.3, 0.7, inside_model, outside_model)

        # Call the render method
        self.assertEqual(window_model.render(0.2), colors.BLUE)
        # self.assertEqual(window_model.render(0.2), colors.RED)
        self.assertEqual(window_model.render(0.2), colors.BLUE)


class TestFlame(unittest.TestCase):
    @patch('random.uniform', side_effect=[0.1, 0.9])
    def test_update(self, mock_uniform):
        # Create an instance of Flame
        flame_instance = Flame("TestFlame")
        #
        # # Call update method with the initial after first flicker
        # flame_instance.update(0.2)
        #
        # # Check if the model was updated with the expected values
        # expected_lower = 0.1
        # expected_upper = 0.9
        # self.assertEqual(flame_instance.model.from_min, expected_lower)
        # self.assertEqual(flame_instance.model.from_max, expected_upper)


if __name__ == '__main__':
    unittest.main()
