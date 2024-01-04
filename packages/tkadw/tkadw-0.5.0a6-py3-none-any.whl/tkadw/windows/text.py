from .drawwidget import AdwDrawWidget


class AdwText(AdwDrawWidget):
    id = "text"

    def __init__(self,
                 *args,
                 drawmode: int = 1,
                 text: str = "",
                 radius: int = 14,
                 font=None,
                 show=...,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.args(
            drawmode=drawmode,
            back="#ffffff",
            back_focus="#ffffff",
            border="#e6e6e6",
            border_focus="#ebebeb",
            border_width=1,
            border_width_focus=1,
            bottomsheet="#9c9c9c",
            bottomsheet_focus="#005fb8",
            bottomsheet_width=1,
            bottomsheet_width_focus=2,
            radius=radius,
            label_text=text,
            text="#18191c",
            text_focus="#18191c",
        )

        self.default_palette()

        from tkinter import Text

        if font is None:
            from tkinter.font import nametofont
            font = nametofont("TkDefaultFont")
        self.inputwidget = Text(self, borderwidth=0, insertwidth=1, font=font)

    def _draw(self, event=None):
        super()._draw(event)
        if self._is_focus:
            __back = self._back_focus
            __border = self._border_focus
            __border_width = self._border_width_focus
            __bottomsheet = self._bottomsheet_focus
            __bottomsheet_width = self._bottomsheet_width_focus
            __text = self._text_focus
        else:
            __back = self._back
            __border = self._border
            __border_width = self._border_width
            __bottomsheet = self._bottomsheet
            __bottomsheet_width = self._bottomsheet_width
            __text = self._text
        try:
            self.inputwidget.configure(background=__back, foreground=__text, selectforeground=__text,
                                       insertbackground=__text)
        except:
            pass

        # 绘制框架
        if self._drawmode == 0:
            self.roundrect_draw(
                x=0, y=0,
                width=self.winfo_width(), height=self.winfo_height(),
                fill=__border, outline=__border, radius=self._radius + 2, tag="frame_border"
            )
            self._frame_border = "frame_border"
            self.roundrect_draw(
                x=__border_width, y=__border_width,
                width=self.winfo_width() - 2 * __border_width,
                height=self.winfo_height() - 2 * __border_width,
                fill=__back, outline=__back, radius=self._radius, tag="frame"
            )
        elif self._drawmode == 1:
            self.roundrect2_draw(
                x1=0, y1=0,
                x2=self.winfo_width() - __border_width,
                y2=self.winfo_height() - __border_width,
                fill=__back, outline=__border, radius=self._radius, tag="frame"
            )
        self._frame = "frame"

        self.text_bottom = self.create_rectangle(__border_width + self._radius / 3,
                                                 self.winfo_height() - __border_width + self._radius,
                                                 self.winfo_width() - __border_width - self._radius / 3,
                                                 self.winfo_height() - __border_width,
                                                 fill=__bottomsheet, outline=__bottomsheet,
                                                 width=__bottomsheet_width)

        try:
            # 绘制输入组件
            self._input = self.create_window(
                self.winfo_width() / 2, self.winfo_height() / 2,
                width=self.winfo_width() - self._radius - __border_width,
                height=self.winfo_height() - __border_width * 2 - 5,
                window=self.inputwidget
            )
        except AttributeError:
            pass

    def _event_focus_in(self, event=None):
        super()._event_focus_in()
        self.inputwidget.focus_set()

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
                if "bottomsheet" in palette[self.id]["default"]:
                    self._bottomsheet = palette[self.id]["default"]["bottomsheet"]
                if "bottomsheet_width" in palette[self.id]["default"]:
                    self._bottomsheet_width = palette[self.id]["default"]["bottomsheet_width"]
                if "fore" in palette[self.id]["default"]:
                    self._text = palette[self.id]["default"]["fore"]
            if "focus" in palette[self.id]:
                if "back" in palette[self.id]["focus"]:
                    self._back_focus = palette[self.id]["focus"]["back"]
                if "border" in palette[self.id]["focus"]:
                    self._border_focus = palette[self.id]["focus"]["border"]
                if "border_width" in palette[self.id]["focus"]:
                    self._border_width_focus = palette[self.id]["focus"]["border_width"]
                if "bottomsheet" in palette[self.id]["focus"]:
                    self._bottomsheet_focus = palette[self.id]["focus"]["bottomsheet"]
                if "bottomsheet_width" in palette[self.id]["focus"]:
                    self._bottomsheet_width_focus = palette[self.id]["focus"]["bottomsheet_width"]
                if "fore" in palette[self.id]["focus"]:
                    self._text_focus = palette[self.id]["focus"]["fore"]
        self.update()
