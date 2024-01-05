def customwindow(window=None):
    if window is None:
        from tkinter import _default_root
        window = _default_root
    from .theme import AdwTTitleBar
    from .manager import WindowManager
    manager = WindowManager(window)
    manager.frameless(True)
    del manager
    titlebar = AdwTTitleBar(window)
    titlebar.show()
    return titlebar
