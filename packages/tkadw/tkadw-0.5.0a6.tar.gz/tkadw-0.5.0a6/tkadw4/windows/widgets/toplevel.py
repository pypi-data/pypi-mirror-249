from tkinter import Toplevel
from tkadw4.windows.widgets.adw import Adw


class AdwToplevel(Toplevel, Adw):
    def __init__(self, *args, master=None, title: str = "adw", config: bool = False,
                 dark: bool = True, dark_with_refresh: bool = False,
                 wincaption=None, **kwargs):
        super().__init__(*args, **kwargs)

