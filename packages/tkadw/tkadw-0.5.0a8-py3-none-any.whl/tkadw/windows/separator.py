from .drawwidget import AdwDrawWidget
from tkinter import HORIZONTAL, VERTICAL


class AdwSeparator(AdwDrawWidget):

    id = "separator"

    def __init__(self,
                 *args,
                 border_width=1,
                 rounded: bool = True,
                 orient=VERTICAL,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.attr(
            border_width=border_width,
            rounded=rounded,
            fore="#d0d0d0",
            orient=orient
        )

        self.default_palette()

    def _draw(self, event=None):
        super()._draw(event)

        if self._orient == VERTICAL:
            self._line = self.create_line(
                self._border_width,
                self.winfo_height() / 2,
                self.winfo_width() - self._border_width,
                self.winfo_height() / 2,
                width=self._border_width,
                fill=self._fore,
            )
        elif self._orient == HORIZONTAL:
            self._line = self.create_line(
                self.winfo_width() / 2,
                self._border_width,
                self.winfo_width() / 2,
                self.winfo_height() - self._border_width,
                width=self._border_width,
                fill=self._fore,
            )

        if self._rounded:
            self.itemconfigure(self._line, capstyle="round", joinstyle="round", smooth=True)

    def default_palette(self):
        pass

    def palette(self, palette: dict):
        if self.id in palette:
            if "rounded" in palette[self.id]:
                self._rounded = palette[self.id]["rounded"]
            if "border_width" in palette[self.id]:
                self._border_width = palette[self.id]["border_width"]
            if "fore" in palette[self.id]:
                self._fore = palette[self.id]["fore"]
        self.update()
