import math
import random

from .colors import add, blend, BLACK, RED, YELLOW
from .utils import map_value


class Model:
    """
    Base class for creating color models to be used in graphical rendering.

    The `Model` class serves as the base class for creating color models that can be used in graphical rendering.
    Subclasses of `Model` are expected to implement the `render` method, which defines how the model should
    produce colors at different positions. Additionally, models that change with time (animations) can implement
    the `update` method to adjust their state to a specified timestamp.

    Parameters:
    - `name` (str): Name of the `Model` instance, useful for debugging

    Methods:
    - `update(timestamp_ms: float)`: Updates the model to the specified timestamp.
      Models that change with time (animations) will need to implement this function.
    - `render(pos: float) -> Tuple[int, int, int]`: Returns the color to be displayed at the specified position.
    ```

    Note:
    - Subclasses of `Model` should implement the `render` method to define the model's behavior.
    - Models that change with time can implement the `update` method to adjust their state to a specified timestamp.
    - If a model does not change with time, the `update` method does not need to be implemented.
    """

    def __init__(self, name: str):
        """
        :param name: Name of this model, shown in debug messages
        """
        self.name = name

    def update(self, timestamp_ms: float):
        """
        Updates the model to the specified timestamp. Usually a renderer will get the time
        of rendering and use the same time stamp to update all models.

        Models that change with time (animations) will need to implement this function.
        Models that do not change with time do not need to implement this method.

        :param timestamp_ms: the time in milliseconds to which to adjust the model
        """
        pass

    def render(self, pos: float) -> tuple:
        """
        Returns the color that should be displayed at the specified pos at the current time.

        :param pos: position of the pixel to be rendered (0.0 - 1.0)
        :return: color
        """
        return BLACK


class Solid(Model):
    """
    Represents a solid color pattern for graphical rendering.

    The `Solid` class creates a model that produces a consistent color across all positions. This is useful for
    creating static color patterns or backgrounds.

    Parameters:
    - `name` (str): Name of the `Solid` instance, shown in debug messages.
    - `color` (tuple): Color of the solid model specified as an RGB tuple.

    Methods:
    - `render(pos: float) -> Tuple[int, int, int]`: Returns the constant color defined by the `Solid` model.
    """

    def __init__(self, name, color: tuple):
        """
        :param name: Name of this model, shown in debug messages,
        :param color: Color of this solid model
        """
        self.color = color
        super().__init__(name)

    def render(self, pos: float):
        return self.color


class Gradient(Model):
    """
    Represents a gradient color pattern transitioning from one color to another.

    The `Gradient` class creates a model that produces a smooth transition of colors between two specified colors.

    Parameters:
    - `name` (str): Name of the `Gradient` instance, shown in debug messages.
    - `c1` (tuple): First color of the gradient specified as an RGB tuple.
    - `c2` (tuple): Second color of the gradient specified as an RGB tuple.

    Methods:
    - `render(pos: float) -> Tuple[int, int, int]`: Returns the color of the gradient at the specified position.

    Usage:
    ```python
    # Create a gradient model transitioning from red to green
    red_to_green = Gradient("RedToGreen", colors.RED, colors.GREEN)
    ```
    """

    def __init__(self, name: str, c1: tuple, c2: tuple):
        """
        :param name: Name of this model, shown in debug messages
        :param c1: First color of the gradient
        :param c2: Second color of the gradient
        """
        self.c1 = c1
        self.c2 = c2
        super().__init__(name)

    def render(self, pos: float):
        return blend(self.c1, self.c2, pos)


class MultiGradient(Model):
    """
    Represents a gradient color pattern with variable number of color points.

    The `MultiGradient` class creates a model that produces a gradient color pattern. Unlike the `Gradient` class,
    this model supports multiple color points, allowing for a more complex transition between colors. The number of
    defined color points is variable, and the gradient is linearly interpolated between adjacent color points.

    Parameters:
    - `name` (str): Name of the `MultiGradient` instance, shown in debug messages.
    - `color_list` (list): List of color tuples specifying the gradient color points.

    Methods:
    - `render(pos: float) -> Tuple[int, int, int]`: Returns the color of the gradient at the specified position.

    Usage:
    ```python
    # Create a multi-gradient model with three color points
    rainbow_model = MultiGradient("Rainbow", [colors.RED, colors.GREEN, colors.BLUE])
    """
    def __init__(self, name: str, color_list: list):
        self.color_list = color_list
        super().__init__(name)

    def render(self, pos: float):
        color_pos = pos * (len(self.color_list) - 1)
        lower = math.floor(color_pos)
        upper = math.ceil(color_pos)

        # Linearly interpolate from the lower color to the upper color. If same, quick return.
        if upper == lower:
            return self.color_list[lower]

        ratio = (color_pos - lower) / (upper - lower)
        color = blend(self.color_list[lower], self.color_list[upper], ratio)
        return color


class Map(Model):
    """
    Map a range from a model into a different range.

    The `Map` class provides a way to map a range from a given model into a different range. This can be useful
    when you want to take a subset of the original model's range and map it into a specific portion of the range
    of the resulting model.

    For example, creating a `Map(gradient, 0.0, 0.5, 0.9, 1.0)` would create a new model with the first half
    of the gradient mapped into the final 10% of the range of the resulting model.

    Parameters:
    - `name` (str): Name of the `Map` instance, used in debug messages.
    - `from_min` (float): Minimum value of the range to map from.
    - `from_max` (float): Maximum value of the range to map from.
    - `to_min` (float): Minimum value of the range to map to.
    - `to_max` (float): Maximum value of the range to map to.
    - `model` (Model): The original model to map.

    Methods:
    - `update(timestamp_ms: float)`: Update the internal state of the model.
    - `render(pos: float) -> Tuple[int, int, int]`: Obtain the color at a given position.

    Usage:
    ```python
    gradient_model = Gradient("TestGradient", (255, 0, 0), (0, 255, 0))
    mapped_model = Map("MappedGradient", 0.0, 0.5, 0.9, 1.0, gradient_model)

    # Render the mapped model at a specific position
    result_color = mapped_model.render(0.95)
    ```

    Note:
    - If the specified position is outside the mapped range (`to_min` to `to_max`), the default color is black.
    """
    def __init__(self, name: str, from_min, from_max, to_min, to_max, model: Model):
        self.from_min = from_min
        self.from_max = from_max
        self.to_min = to_min
        self.to_max = to_max
        self.model = model
        super().__init__(name)

    def update(self, timestamp_ms: float):
        self.model.update(timestamp_ms)

    def render(self, pos: float):
        if self.to_min <= pos <= self.to_max:
            from_pos = map_value(pos, self.to_min, self.to_max, self.from_min, self.from_max)
            return self.model.render(from_pos)

        # Position is outside the range, default to black
        return BLACK

    def set_from_range(self, from_min: float, from_max: float) -> None:
        """
        Set the "from" range.

        :param from_min: new minimum value of the range
        :param from_max: new maximum value of the range
        """
        self.from_min = from_min
        self.from_max = from_max


class Triangle(Model):
    """
    Triangle is a model that creates a range of colors from black to the specified color and then back to black.
    The full color is reached at the midpoint of the specified range. Outside the range, the model returns the
    color black.

    Parameters:
    - `name` (str): The name of the Triangle instance, used in debug messages.
    - `range_min` (float): The minimum position value of the range where colors will be generated.
    - `range_max` (float): The maximum position value of the range where colors will be generated.
    - `color` (tuple): The RGB color tuple representing the full color of the triangle at the midpoint.

    Methods:
    - `render(pos: float) -> Tuple[int, int, int]`: Obtain the color at a given position within the specified range.

    Usage:
    ```python
    # Creating a Triangle instance
    triangle_model = Triangle("MyTriangle", 0.2, 0.8, (255, 0, 0))

    # Rendering the model at a specific position
    result_color = triangle_model.render(0.5)
    ```

    The `Triangle` model generates a triangle-shaped color gradient within the specified range, blending from black to
    the specified color and back to black.
    """
    def __init__(self, name: str, range_min: float, range_max: float, color: tuple):
        self.range_min = range_min
        self.range_max = range_max
        self.color = color
        super().__init__(name)

    def render(self, pos: float):
        if pos < self.range_min or pos > self.range_max:
            return BLACK

        mid_point = (self.range_min + self.range_max) / 2

        if pos <= mid_point:
            # Rising side of triangle
            ratio = map_value(pos, self.range_min, mid_point, 0.0, 1.0)
            return blend(BLACK, self.color, ratio)
        else:
            # Falling side of triangle
            ratio = map_value(pos, mid_point, self.range_max, 1.0, 0.0)
            return blend(BLACK, self.color, ratio)


class Reverse(Model):
    """
    Create a new model that is the reverse of the input model.

    Parameters:
    - `name` (str): Name of the `Reverse` instance, used in debug messages.
    - `model` (Model): The input model whose rendering will be reversed.

    Methods:
    - `update(timestamp_ms: float)`: Update the internal state of the input model.
    - `render(pos: float) -> Tuple[int, int, int]`: Obtain the reversed color at a given position.

    """
    def __init__(self, name: str, model: Model):
        self.model = model
        super().__init__(name)

    def update(self, timestamp_ms: float):
        self.model.update(timestamp_ms)

    def render(self, pos: float):
        return self.model.render(1.0 - pos)


class Add(Model):
    """
    Add models together

    The `Add` class allows you to combine multiple models by adding their colors together. The resulting color
    is obtained by summing the colors of corresponding pixels from each model. The addition operation is
    constrained to ensure that each pixel channel (red, green, blue) does not exceed full brightness.

    Parameters:
    - `name` (str): Name of the `Add` instance, used in debug messages.
    - `models` (list[Model]): List of models to be added together.

    Methods:
    - `render(pos: float) -> Tuple[int, int, int]`: Obtain the combined color at a given position.

    Usage:
    ```python
    gradient_model = Gradient("Gradient1", (255, 0, 0), (0, 255, 0))
    solid_model = Solid("Solid1", (0, 0, 255))

    # Create an Add model by combining the gradient and solid models
    combined_model = Add("CombinedModel", [gradient_model, solid_model])

    Note:
    - The addition operation is performed for each pixel channel (red, green, blue) independently.
    - The resulting color is constrained to ensure that each channel does not exceed full brightness.
    """

    def __init__(self, name: str, models: list[Model]):
        self.models = models
        super().__init__(name)

    def update(self, timestamp_ms):
        for model in self.models:
            model.update(timestamp_ms)

    def render(self, pos: float):
        model_colors = [m.render(pos) for m in self.models]
        return add(*model_colors)


class Window(Model):
    """
    A model that creates a window effect by combining two models based on a specified position range.

    The `Window` class represents a virtual window where two different models are rendered based on the position
    within a specified range. The inside of the window is rendered using one model (`inside_model`), and the outside
    of the window is rendered using another model (`outside_model`).

    Parameters:
    - `name` (str): Name of the `Window` instance, shown in debug messages.
    - `range_min` (float): Minimum position value of the window range.
    - `range_max` (float): Maximum position value of the window range.
    - `inside_model` (Model): The model to render inside the window range.
    - `outside_model` (Model): The model to render outside the window range.

    Methods:
    - `update(timestamp_ms: float)`: Update the internal state of the `Window` and its models.
    - `render(pos: float) -> Tuple[int, int, int]`: Obtain the color at a given position.

    Usage:
    ```python
    # Create two models for inside and outside the window
    inside_model = Gradient("InsideGradient", (255, 0, 0), (0, 255, 0))
    outside_model = Solid("OutsideSolid", (0, 0, 255))

    # Create a window that transitions from the inside gradient to the outside solid color
    window_model = Window("WindowModel", 0.3, 0.7, inside_model, outside_model)
    """
    def __init__(self, name: str, range_min: float, range_max: float, inside_model: Model, outside_model: Model):
        self.range_min = range_min
        self.range_max = range_max
        self.inside_model = inside_model
        self.outside_model = outside_model
        super().__init__(name)

    def update(self, timestamp_ms):
        self.inside_model.update(timestamp_ms)
        self.outside_model.update(timestamp_ms)

    def render(self, pos):
        if self.range_min <= pos <= self.range_max:
            return self.inside_model.render(pos)
        else:
            return self.outside_model.render(pos)
        pass


class Flame(Model):
    COLOR1 = blend(RED, YELLOW, 0.5)
    COLOR2 = blend(RED, YELLOW, 0.7)
    COLOR3 = blend(RED, YELLOW, 0.9)
    PERIOD_MS = 110

    last_update_ms = 0.0
    gradient = MultiGradient("flame-multigradient", [BLACK, COLOR1, COLOR2, COLOR3, COLOR2, COLOR1, BLACK])
    model = Map("flame-map", 0.0, 1.0, 0.0, 1.0, gradient)

    def __init__(self, name: str):
        super().__init__(name)

    def update(self, timestamp_ms):
        # Only update the model occasionally to create the "flickering" effect
        if (timestamp_ms - self.last_update_ms) > self.PERIOD_MS:
            self.last_update_ms = timestamp_ms

            lower = random.uniform(0.0, 0.2)
            upper = random.uniform(0.8, 1.0)

            self.model.set_from_range(lower, upper)

            self.model.update(timestamp_ms)

    def render(self, pos: float):
        return self.model.render(pos)

# ##### IDEAS #####

#  Dim
#  Adjust the brightness of the color down by the provided percent
#
#  Constructors:
#    Dim(dimPercent, model) - dims all colors of the underlying model by dimPercent, expressed as 0.0-1.0
#
#  Requires input model
#  Position and time independent


#  Brighten
#  Increases the brightness of the color up by the provided percent, no R, G, or B will exceed 255
#  (Note: is this a new "Filter" category of models?)
#
#  Constructors:
#    Brighten(brightenPercent, model) - brightens all colors of the  model by brightenPercent, expressed as 0.0-1.0
#
#  Requires input model
#  Position and time independent


#  Firefly
#  A firefly (small light band? needs definition) flits around in a specified range with
#  some sort of speed parameters


#  Matrix
#  Green spots flow from one end of the strip to the other.
#  Can experiment with varying rates, sizes, brightnesses, hues.
#
#  Position and time dependent.


#  Blend
#  Blend two models together. Details TBD, but options include LERP, add, etc.
#
#  Requires two input models.
#  Position and time independent.


#  Blur
#  Performs some sort of convolution around a position to blur the colors.
#
#  Requires input model.
#  Position and time independent.


#  Lava lamp
#  Simulate a lava lamp.
#
#  Direction - up/down
#  Color

#  Warp core
#  Simulate a Star Trek warp core.
#
#  Direction - up/down?
#  Color?
#  Speed?


#  Jacob's ladder
#  Simulate the rising electrical arc of a Jacob's ladder.
#
#  Color?
#  Speed?
