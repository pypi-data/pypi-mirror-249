from .drawwidget import AdwDrawWidget
from tkinter import Event


class AdwSizegrip(AdwDrawWidget):
    id = "sizegrip"

    def __init__(self, *args, width=16, height=16, cursor="sizing", **kwargs):
        super().__init__(*args, width=width, height=height, cursor=cursor, **kwargs)
        self.bind("<Button-1>", self._event_button1)
        self.bind("<B1-Motion>", self._event_button_motion)
        self.width, self.height, self.startx, self.starty = 0, 0, 0, 0

        self.attr(
            fore="grey",
            partsize=1,
        )

    def _draw(self, event=None):
        super()._draw()

        parts = 4

        for index_x in range(1, parts + 1):
            for index_y in range(1, parts + 1):
                self.create_rectangle(
                    (self.winfo_width() / (parts + 1)) * index_x - self._partsize / 2,
                    (self.winfo_height() / (parts + 1)) * index_y - self._partsize / 2,
                    (self.winfo_width() / (parts + 1)) * index_x + self._partsize / 2,
                    (self.winfo_height() / (parts + 1)) * index_y + self._partsize / 2,
                    outline=self._fore, fill=self.cget("bg")
                )

    def _event_button1(self, event: Event):
        from tkinter import _default_root
        self.startx, self.starty = event.x_root, event.y_root
        self.width, self.height = _default_root.winfo_width(), _default_root.winfo_height()

    def _event_button_motion(self, event: Event):
        from tkinter import _default_root
        new_width = self.width + (event.x_root - self.startx)
        new_height = self.height + (event.y_root - self.starty)
        if new_width < 0:
            new_width = 0
        if new_height < 0:
            new_height = 0
        _default_root.geometry(f"{round(new_width)}x{round(new_height)}")

    def palette(self, palette: dict):
        if self.id in palette:
            if "fore" in palette[self.id]:
                self._fore = palette[self.id]["fore"]
