from .frame import AdwFrame
from tkinter import CENTER


class AdwTitleBar(AdwFrame):
    id = "titlebar"

    def __init__(self, *args, width=300, height=45, **kwargs):
        super().__init__(*args, **kwargs)

        from tkinter import _default_root

        self.attr(
            back="#fdfdfd",
            border="#ededed",
            button_size=25,
            close="red",
            fore="#000000",
            title_anchor=CENTER,
            title_text=_default_root.title()
        )

        from .closebutton import AdwCloseButton
        from .label import AdwLabel

        from tkinter import PhotoImage

        self._iconphoto = _default_root.iconbitmap()
        print(self._iconphoto)

        self._closebutton = AdwCloseButton(self, width=self._button_size, height=self._button_size, text="╳")
        self._closebutton.pack(side="right", anchor="e", padx=5, pady=5)

        self._title = AdwLabel(self, text=self._title_text)
        self._title.pack(anchor=self._title_anchor, padx=5, pady=5)

        self.frame.configure(width=width, height=height)

        from .dragarea import bind_window_move
        bind_window_move(self)
        bind_window_move(self._title)

        self.default_palette()

    def _draw(self, event=None):
        self._radius = 0
        self._border_width = 0
        super()._draw(event)
        try:
            self._title.text(self._title_text)
            if self._title.winfo_ismapped():
                self._title.pack(anchor=self._title_anchor)
        except:
            pass
        self.configure(background=self._back)
        self.border = self.frame.create_line(0, 2, self.winfo_width(), 2, fill=self._border)

    def title(self, text: str = None):
        if text:
            self._title_text = text
        else:
            return self._title_text

    def titlewidget(self):
        return self._title

    def palette(self, palette: dict):
        if self.id in palette:
            if "back" in palette[self.id]:
                self._back = palette[self.id]["back"]
            if "border" in palette[self.id]:
                self._border = palette[self.id]["border"]
            if "fore" in palette[self.id]:
                self._fore = palette[self.id]["fore"]
            if "title_anchor" in palette[self.id]:
                self._title_anchor = palette[self.id]["title_anchor"]
        self.update()
        try:
            self._title.palette(palette)
            self._closebutton.palette(palette)
        except:
            pass

    def show(self, *args, **kwargs):
        self.pack(*args, fill="x", side="top", **kwargs)
