from .drawwidget import AdwDrawWidget
from .drawengine import AdwDrawEngine
from tkinter import Frame
from .base import AdwBase


class AdwFrame(Frame, AdwBase):
    id = "frame"

    def __init__(self,
                 master=None,
                 *args,
                 width=300,
                 height=200,
                 drawmode: int = 1,
                 radius: int = 14,
                 **kwargs,
                 ):
        from .root import root
        master = root(master)

        self.frame = AdwDrawEngine(master, width=width, height=height)
        self.frame.bind("<Configure>", self.update, add="+")

        super().__init__(master=self.frame, *args, **kwargs)

        self.attr(
            drawmode=drawmode,
            back="#fdfdfd",
            border="#ededed",
            border_width=1,
            radius=radius,
        )

        self.default_palette()

    def update(self, event=None):
        super().update()
        self.frame.update()
        self._draw(event)

    def default_palette(self):
        pass

    def palette(self, palette: dict):
        if self.id in palette:
            if "radius" in palette[self.id]:
                self._radius = palette[self.id]["radius"]
            if "back" in palette[self.id]:
                self._back = palette[self.id]["back"]
            if "border" in palette[self.id]:
                self._border = palette[self.id]["border"]
            if "border_width" in palette[self.id]:
                self._border_width = palette[self.id]["border_width"]
        self.update()
        for child in self.winfo_children():
            if hasattr(child, "palette"):
                child.palette(palette)
                child.update()

    def _draw(self, event=None):
        self.frame.configure(background=self.frame.master.cget("bg"), highlightbackground=self.frame.master.cget("bg"))
        self.configure(background=self._back)
        self.frame.delete("all")

        # 绘制框架
        if self._drawmode == 0:
            self.frame.roundrect_draw(
                x=0, y=0,
                width=self.winfo_width(), height=self.winfo_height(),
                fill=self._border, outline=self._border, radius=self._radius + 2, tag="frame_border"
            )
            self._frame_border = "frame_border"
            self.frame.roundrect_draw(
                x=self._border_width, y=self._border_width,
                width=self.frame.winfo_width() - 2 * self._border_width,
                height=self.frame.winfo_height() - 2 * self._border_width,
                fill=self._back, outline=self._back, radius=self._radius, tag="frame"
            )
        elif self._drawmode == 1:
            self.frame.roundrect2_draw(
                x1=0, y1=0,
                x2=self.frame.winfo_width() - self._border_width,
                y2=self.frame.winfo_height() - self._border_width,
                fill=self._back, outline=self._border, radius=self._radius, tag="frame"
            )
        self._frame = "frame"

        self._widget = self.frame.create_window(
            self.frame.winfo_width() / 2, self.frame.winfo_height() / 2,
            window=self,
            anchor="center",
            width=self.frame.winfo_width() - self._border_width - self._radius / 2,
            height=self.frame.winfo_height() - self._border_width - self._radius / 2
        )

    # 重实现
    def pack_info(self):
        return self.frame.pack_info()

    def pack_forget(self):
        self.frame.pack_forget()

    def pack_slaves(self):
        return self.frame.pack_slaves()

    def pack_propagate(self, flag):
        self.frame.pack_propagate(flag)

    def pack_configure(self, *args, **kwargs):
        self.frame.pack_configure(*args, **kwargs)

    pack = pack_configure

    def place_info(self):
        return self.frame.place_info()

    def place_forget(self):
        self.frame.place_forget()

    def place_slaves(self):
        self.frame.place_slaves()

    def place_configure(self, *args, **kwargs):
        self.frame.pack_configure(*args, **kwargs)

    place = place_configure

    def put_info(self):
        return self.frame.put_info()

    def put_forget(self):
        self.frame.put_forget()

    def put_configure(self, *args, **kwargs):
        self.frame.put_configure(*args, **kwargs)

    put = put_configure

    def grid_info(self):
        return self.frame.grid_info()

    def grid_forget(self):
        self.frame.grid_forget()

    def grid_slaves(self, row=..., column=...):
        return self.frame.grid_slaves(row, column)

    def grid_propagate(self, flag):
        self.frame.grid_propagate(flag)

    def grid_configure(self, *args, **kwargs):
        self.frame.grid_configure(*args, **kwargs)
