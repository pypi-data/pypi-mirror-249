def customwindow(window=None):
    from .root import root
    window = root(window)
    from .theme import AdwTTitleBar
    from .manager import WindowManager
    manager = WindowManager(window)
    manager.frameless(True)
    del manager
    titlebar = AdwTTitleBar(window)
    titlebar.show()
    return titlebar
