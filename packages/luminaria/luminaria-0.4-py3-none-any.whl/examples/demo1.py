import wx

from luminaria.animations import Rotate
from luminaria.colors import BLUE, GREEN, RED, YELLOW
from luminaria.models import Gradient, Map, Window
from luminaria.renderer.wx_renderer import Renderer

PIXELS_COUNT = 50


def make_model():
    grad_left = Gradient("grad-right", BLUE, GREEN)
    grad_right = Gradient("grad-left", RED, YELLOW)

    rot_left = Rotate("rotate down", -3000, grad_left)
    rot_right = Rotate("rotate up", 1000, grad_right)

    map_left = Map("map left", 0.0, 1.0, 0.0, 0.3, rot_left)
    map_right = Map("map right", 0.0, 1.0, 0.3, 1.0, rot_right)

    window = Window("window", 0.0, 0.3, map_left, map_right)

    rot_window = Rotate("rotate window", -10000, window)

    return rot_window


if __name__ == "__main__":
    app = wx.App(False)
    wx_renderer = Renderer(PIXELS_COUNT, make_model())
    app.MainLoop()
