import wx

from luminaria.animations import Pulsate
from luminaria.colors import BLACK, BLUE, GREEN, RED
from luminaria.models import Add, Gradient, Solid
from luminaria.renderer.wx_renderer import Renderer

PIXELS_COUNT = 50


def make_model():
    red_gradient = Gradient("grad_red", BLACK, RED)
    blue_gradient = Gradient("grad_red", BLUE, BLACK)
    green_solid = Solid("green solid", GREEN)
    sum3 = Add("Add", [red_gradient, blue_gradient, green_solid])
    pulsation = Pulsate("Pulsation", dimmest=0.2, brightest=1.0, dim_ms=1000, brighten_ms=2000, model=sum3)

    return pulsation


if __name__ == "__main__":
    app = wx.App(False)
    wx_renderer = Renderer(PIXELS_COUNT, make_model())
    app.MainLoop()
