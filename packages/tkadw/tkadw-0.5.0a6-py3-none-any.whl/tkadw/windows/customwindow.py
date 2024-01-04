def customwindow(window):
    """
    暂时只支持AdwMainWindow，不支持tkinter.Tk
    """
    from .theme import AdwTTitleBar
    from .window import AdwMainWindow
    window.frameless(True)
    titlebar = AdwTTitleBar(window)
    titlebar.show()
    return titlebar
