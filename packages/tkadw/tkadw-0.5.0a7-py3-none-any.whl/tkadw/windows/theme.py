from os import environ

from json import dumps

try:
    from .themes.win11 import AdwWin11Theme

    environ["ADWTHEME"] = dumps(AdwWin11Theme().get())
    environ["ADWTHEME.MODE"] = "light"
except:
    pass


def theme(name=None):
    if name:
        if "ADWTHEME" in environ:
            from json import dumps
            environ["ADWTHEME"] = dumps(name)
    else:
        if "ADWTHEME" in environ:
            from json import loads
            return loads(environ["ADWTHEME"])


def theme_mode(mode=None):
    if mode:
        environ["ADWTHEME.MODE"] = mode
    else:
        if "ADWTHEME" in environ:
            return environ["ADWTHEME.MODE"]


def set_default_theme(themename, thememode="system", window=None):
    from .themes.themebuilder import AdwSimpleThemeBuilder
    from .themes.theme import AdwTheme
    if themename == "win11":
        theme(AdwWin11Theme().get())
    elif issubclass(themename.__class__, AdwSimpleThemeBuilder) or issubclass(themename.__class__, AdwTheme):
        theme(themename.get())
    else:
        theme(themename)
    if thememode == "system":
        try:
            from darkdetect import isDark
        except ModuleNotFoundError:
            pass
        else:
            if isDark():
                theme_mode("dark")
            else:
                theme_mode("light")
    else:
        theme_mode(thememode)

    if window:
        if hasattr(window, "palette"):
            window.palette(theme()[theme_mode()])

            window.update()
        else:
            window.configure(bg=theme()[theme_mode()]["window"]["back"])

        for child in window.winfo_children():
            if hasattr(child, "palette"):
                child.palette(theme()[theme_mode()])
                child.update()


class AdwThemed(object):
    def dark_palette(self):
        if theme():
            self.palette(theme()["dark"])

    def default_palette(self):
        if theme():
            self.palette(theme()[theme_mode()])

    def light_palette(self):
        if theme():
            if theme_mode():
                self.palette(theme()["light"])


from .button import AdwButton


class AdwTButton(AdwThemed, AdwButton):
    pass


from .circularbutton import AdwCircularButton


class AdwTCircularButton(AdwThemed, AdwCircularButton):
    pass


from .entry import AdwEntry


class AdwTEntry(AdwThemed, AdwEntry):
    pass


from .frame import AdwFrame


class AdwTFrame(AdwThemed, AdwFrame):
    pass


from .label import AdwLabel


class AdwTLabel(AdwThemed, AdwLabel):
    pass


from .window import AdwMainWindow


class _AdwTMainWindow(AdwThemed, AdwMainWindow):
    def dark(self, enable: bool, width_icon=True):
        if width_icon:
            self.icon(enable)
        if enable:
            self.styles(["dark"])
        else:
            self.styles(["light"])

    def theme(self, themename, thememode="system"):
        set_default_theme(themename=themename, thememode=thememode, window=self)


class AdwTMainWindow(_AdwTMainWindow, ):
    pass


from .menubar import AdwMenuBar


class AdwTMenuBar(AdwThemed, AdwMenuBar):
    pass


def create_root_themed_menubar():
    from tkinter import _default_root
    _ = AdwTMenuBar(_default_root)
    _.show()
    return _


from .separator import AdwSeparator


class AdwTSeparator(AdwThemed, AdwSeparator):
    pass


from .sizegrip import AdwSizegrip


class AdwTSizegrip(AdwThemed, AdwSizegrip):
    pass


from .text import AdwText


class AdwTText(AdwThemed, AdwText):
    pass


from .titlebar import AdwTitleBar


class AdwTTitleBar(AdwThemed, AdwTitleBar):
    pass


from .window import AdwWindow


class AdwTWindow(_AdwTMainWindow, AdwWindow):
    pass


from .mdi import AdwWindowsMDI


class AdwTWindowsMDI(AdwThemed, AdwWindowsMDI):
    pass
