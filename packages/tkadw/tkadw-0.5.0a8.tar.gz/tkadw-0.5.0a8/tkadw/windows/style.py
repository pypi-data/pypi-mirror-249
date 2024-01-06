LIGHT = "light"
DARK = "dark"


class WindowStyle:
    def __init__(self, master=None):
        """
        窗口样式
        _Windows_系统需安装_pywinstyles_库
        """
        from .root import root
        self.master = root(master)

    def _style_mac(self, stylename: str):
        """
        设置MacOS平台下的窗口样式

        Args:
            stylename (str): 样式名称参见https://wiki.tcl-lang.org/page/MacWindowStyle

        """
        from os import system
        if stylename == "dark":
            system("defaults write -g NSRequiresAquaSystemAppearance -bool No")
        elif stylename == "light":
            system("defaults delete -g NSRequiresAquaSystemAppearance")
        else:
            self.master.call("::tk::unsupported::MacWindowStyle", "style", self.master._w, stylename)

    def _style_win(self, stylename: str):
        """
        设置Windows平台下的窗口样式

        Args:
            stylename (str): 样式名称参见https://pypi.org/project/pywinstyles
        """
        try:
            from pywinstyles import apply_style
            apply_style(self.master, stylename)
        except ModuleNotFoundError as error:
            print(error)

    def style(self, stylename: str):
        """
        设置窗口样式，暂时只支持Windows和MacOs平台

        Args:
            stylename (str): 样式名称，共有样式名_light_、_dark_
        """
        from sys import platform
        if platform == "win32" or platform == "cygwin":
            self._style_win(stylename)
        elif platform == "darwin":
            self._style_mac(stylename)


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    windowstyle = WindowStyle()
    windowstyle.style("dark")

    root.mainloop()
