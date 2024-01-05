import time

import board

from luminaria.animations import Rotate
from luminaria.colors import BLUE, GREEN, ORANGE, RED, VIOLET, WHITE, YELLOW
from luminaria.models import MultiGradient, Solid
from luminaria.renderer.circuitpython_neopixel_renderer import Renderer

# Setup neopixel sequence
print("Initializing pixels")
PIXELS_PIN = board.GP28
PIXELS_COUNT = 50
BRIGHTNESS = 1.0
renderer = Renderer(PIXELS_PIN, PIXELS_COUNT, brightness=BRIGHTNESS)

# Flash the pixels white for a short time
renderer.model = Solid("Solid white", WHITE)
renderer.render()
time.sleep(0.2)

# Set up the model for the pixels
print("Setting up lighting model")
gradient = MultiGradient("Gradient rainbow", [RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET, RED])
rotate = Rotate("Rotation", 2500, gradient)
renderer.model = rotate

print("Starting loop")
while True:
    renderer.render()
    time.sleep(.010)
