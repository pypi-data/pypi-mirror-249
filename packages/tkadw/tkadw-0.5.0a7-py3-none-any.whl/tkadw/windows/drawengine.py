from tkinter import Canvas
from .gradient import Gradient, Gradient2
from .roundrect import RoundRect
from .widget import AdwWidget


class AdwDrawEngine(Canvas, AdwWidget):
    id = "drawengine"

    def __init__(
            self,
            *args,
            highlightthickness=0,
            borderwidth=0,
            **kwargs
    ):
        super().__init__(*args, highlightthickness=highlightthickness, borderwidth=borderwidth, **kwargs)

        self.gradient = Gradient()
        self.gradient2 = Gradient2()

        self.roundrect = RoundRect()

    def _draw(self, event=None):
        self.delete("all")

    def update(self, event=None):
        super().update()
        self._draw(event)

    def gradient_draw(self, *args, **kwargs):
        """
        绘制渐变图形
        """
        self.gradient.draw(self, *args, **kwargs)

    def gradient2_draw(self, *args, **kwargs):
        """
        用渐变颜色填充画布
        """
        self.gradient2.draw1(self, *args, **kwargs)

    def gradient_recolor(self, *args, **kwargs):
        """
        修改渐变图形的颜色
        """
        self.gradient.recolor(self, *args, **kwargs)

    def gradient_redraw(self, *args, **kwargs):
        """
        重绘渐变图形
        """
        self.gradient.redraw(self, *args, **kwargs)

    def gradient_resize(self, *args, **kwargs):
        """
        修改渐变图形的位置大小
        """
        self.gradient.resize(self, *args, **kwargs)

    def roundrect_draw(self, *args, **kwargs):
        self.roundrect.draw(self, *args, **kwargs)

    def roundrect2_draw(self, *args, **kwargs):
        self.roundrect.draw2(self, *args, **kwargs)

    def roundrect3_draw(self, x1, y1, ):
        coord = x1, y1, self.winfo_height(), self.winfo_height()
        self.r1 = self.create_arc(x1, y1, self.winfo_height(), self.winfo_height(), )
