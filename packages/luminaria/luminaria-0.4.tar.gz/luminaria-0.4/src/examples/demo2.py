import wx

from luminaria.animations import Pulsate, Rotate
from luminaria.colors import BLUE, RED
from luminaria.models import Gradient, Map, Reverse, Window
from luminaria.renderer.wx_renderer import Renderer

PIXELS_COUNT = 50


def make_model():
    gradient = Gradient("grad", BLUE, RED)
    rot_grad = Rotate("Rotate Gradient", 2500, gradient)
    rev_grad = Reverse("reverse", rot_grad)

    map_left = Map("map left", 0.0, 1.0, 0.0, 0.5, rot_grad)
    map_right = Map("map right", 0.0, 1.0, 0.5, 1.0, rev_grad)

    window = Window("window", 0.0, 0.5, map_left, map_right)
    pulsation = Pulsate("pulsate", 0.2, 1.0, 1000, 1000, window)

    return pulsation


if __name__ == "__main__":
    app = wx.App(False)
    wx_renderer = Renderer(PIXELS_COUNT, make_model())
    app.MainLoop()
