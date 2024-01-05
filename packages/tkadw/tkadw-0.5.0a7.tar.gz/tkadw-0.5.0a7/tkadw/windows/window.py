from tkinter import Tk
from .base import AdwBase
from .run import AdwRun


class AdwMainWindow(AdwBase, Tk):
    id = "window"

    def __init__(self, *args, styles=None, classname="tkadw", **kwargs):
        super().__init__(*args, className=classname, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.is_quit = None

        self.default_palette()

        from .style import WindowStyle
        from .manager import WindowManager

        self.windowstyle = WindowStyle(self)
        self.windowmanager = WindowManager(self)

        if styles:
            self.styles(styles)

        self.icon()

    def custom(self):
        from .customwindow import customwindow
        self.titlebar = customwindow(self)

    def default_palette(self):
        pass

    def frameless(self, enable: bool = None):
        return self.windowmanager.frameless(enable)

    def icon(self, dark=False):
        from .icon import icon
        icon(self, dark=dark)

    def palette(self, palette: dict):
        if self.id in palette:
            if "back" in palette[self.id]:
                self.configure(background=palette[self.id]["back"])

    def quit(self):
        self.is_quit = True
        self.destroy()

    def run(self):
        self.is_quit = False
        while not self.is_quit:
            self.update()

    def styles(self, names: list):
        """
        设置多个窗口样式

        Args:
            names (list): 样式名称
        """
        for style in names:
            self.windowstyle.style(style)


from tkinter import Toplevel


class AdwWindow(Toplevel, AdwMainWindow):
    def __init__(self, *args, styles=None, title: str = "adwite", **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.is_quit = None

        self.title(title)

        self.default_palette()

        from .style import WindowStyle

        self.windowstyle = WindowStyle(self)
        if styles:
            self.styles(styles)

        self.icon()
