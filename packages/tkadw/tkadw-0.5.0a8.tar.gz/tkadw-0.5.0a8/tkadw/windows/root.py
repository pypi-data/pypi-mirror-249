from tkinter import Tk


def root(window) -> Tk:
    if window is None:
        from tkinter import _default_root
        return _default_root
    else:
        return window
