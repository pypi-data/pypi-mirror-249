from .drawwidget import AdwDrawWidget


class AdwCircularButton(AdwDrawWidget):
    id = "circularbutton"

    def __init__(self,
                 *args,
                 command=None,
                 text: str = "",
                 radius: int = 14,
                 width=75, height=75,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        if command is None:
            def _():
                pass

            command = _

        # 初始属性
        self.attr(
            back="#fdfdfd",
            back_hover="#f9f9f9",
            back_down="#fafafa",
            border="#ededed",
            border_hover="#d5d5d5",
            border_down="#ebebeb",
            border_width=1,
            border_width_hover=1,
            border_width_down=1,
            radius=radius,
            label_text=text,
            text="#202020",
            text_hover="#202020",
            text_down="#202020",
        )

        self.bind("<<Click>>", lambda event=None: command())

        self.default_palette()

    def _draw(self, event=None):
        super()._draw(event)
        if self._is_enter:
            if self._is_button:
                __back = self._back_down
                __border = self._border_down
                __border_width = self._border_width_down
                __text = self._text_down
            else:
                __back = self._back_hover
                __border = self._border_hover
                __border_width = self._border_width_hover
                __text = self._text_hover
        else:
            __back = self._back
            __border = self._border
            __border_width = self._border_width
            __text = self._text

        try:
            self._frame = self.create_oval(
                __border_width, __border_width,
                self.winfo_width() - __border_width, self.winfo_height() - __border_width,
                fill=__back, outline=__border, width=__border_width
            )

            # 绘制文字
            self._label = self.create_text(
                self.winfo_width() / 2, self.winfo_height() / 2,
                text=self._label_text, fill=__text
            )
        except:
            pass

    def command(self, func):
        self.bind("<<Click>>", lambda event=None: func())

    def default_palette(self):
        pass

    def palette(self, palette: dict):
        if self.id in palette:
            if "radius" in palette[self.id]:
                self._radius = palette[self.id]["radius"]
            if "default" in palette[self.id]:
                if "back" in palette[self.id]["default"]:
                    self._back = palette[self.id]["default"]["back"]
                if "border" in palette[self.id]["default"]:
                    self._border = palette[self.id]["default"]["border"]
                if "border_width" in palette[self.id]["default"]:
                    self._border_width = palette[self.id]["default"]["border_width"]
                if "fore" in palette[self.id]["default"]:
                    self._text = palette[self.id]["default"]["fore"]
            if "hover" in palette[self.id]:
                if "back" in palette[self.id]["hover"]:
                    self._back_hover = palette[self.id]["hover"]["back"]
                if "border" in palette[self.id]["hover"]:
                    self._border_hover = palette[self.id]["hover"]["border"]
                if "border_width" in palette[self.id]["hover"]:
                    self._border_width_hover = palette[self.id]["hover"]["border_width"]
                if "fore" in palette[self.id]["hover"]:
                    self._text_hover = palette[self.id]["hover"]["fore"]
            if "down" in palette[self.id]:
                if "back" in palette[self.id]["down"]:
                    self._back_down = palette[self.id]["down"]["back"]
                if "border" in palette[self.id]["down"]:
                    self._border_down = palette[self.id]["down"]["border"]
                if "border_width" in palette[self.id]["down"]:
                    self._border_width_down = palette[self.id]["down"]["border_width"]
                if "fore" in palette[self.id]["down"]:
                    self._text_down = palette[self.id]["down"]["fore"]
        self.update()
