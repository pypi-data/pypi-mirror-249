from .drawwidget import AdwDrawWidget


class AdwLabel(AdwDrawWidget):
    id = "label"

    def __init__(self,
                 *args,
                 text: str = "",
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.attr(
            label_text=text,
            text="#18191c"
        )

        self.default_palette()

    def _draw(self, event=None):
        super()._draw(event)

        self.text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2, text=self._label_text, fill=self._text
        )

    def default_palette(self):
        pass

    def text(self, text: str = None):
        if text:
            self._label_text = text
            self.update()
        else:
            return self._label_text

    def palette(self, palette: dict):
        if self.id in palette:
            if "fore" in palette[self.id]:
                self._text = palette[self.id]["fore"]
        self.update()
