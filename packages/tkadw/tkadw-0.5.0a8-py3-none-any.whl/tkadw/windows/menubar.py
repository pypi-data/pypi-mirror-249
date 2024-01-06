from .drawwidget import AdwDrawWidget


class AdwMenuBar(AdwDrawWidget):
    id = "menubar"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attr(
            back="#fdfdfd",
            border="#ededed",
        )

        self.default_palette()

    def _draw(self, event=None):
        super()._draw(event)
        self.configure(background=self._back)
        self.border = self.create_line(0, self.winfo_height() - 1, self.winfo_width(), self.winfo_height() - 1,
                                       fill=self._border)

    def default_palette(self):
        pass

    def update(self):
        super().update()

    def palette(self, palette: dict):
        if self.id in palette:
            if "back" in palette[self.id]:
                self._back = palette[self.id]["back"]
            if "border" in palette[self.id]:
                self._border = palette[self.id]["border"]
        self.update()

    def show(self, *args, **kwargs):
        self.pack(*args, fill="x", side="top", **kwargs)


def create_root_menubar():
    from tkinter import _default_root
    _ = AdwMenuBar(_default_root)
    _.show()
    return _
