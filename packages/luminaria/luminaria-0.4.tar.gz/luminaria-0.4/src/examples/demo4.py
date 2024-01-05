import wx

from luminaria.animations import Rotate
from luminaria.colors import BLUE, GREEN, ORANGE, RED, VIOLET, YELLOW
from luminaria.models import MultiGradient
from luminaria.renderer.wx_renderer import Renderer

PIXELS_COUNT = 50


def make_model():
    gradient = MultiGradient("Gradient rainbow", [RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET, RED])
    rotation = Rotate("Rotation", 7500, gradient)
    return rotation


if __name__ == "__main__":
    app = wx.App(False)
    wx_renderer = Renderer(PIXELS_COUNT, make_model())
    app.MainLoop()
