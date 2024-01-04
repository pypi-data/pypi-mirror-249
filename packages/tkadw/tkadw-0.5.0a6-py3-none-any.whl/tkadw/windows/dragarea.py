from tkinter import Event, Widget, Tk, Frame


x, y = 0, 0


def click(event: Event):
    global x, y
    x, y = event.x, event.y


def move(event: Event, widget: Widget, window: Tk):
    global x, y
    new_x = (event.x - x) + window.winfo_x()
    new_y = (event.y - y) + window.winfo_y()
    if new_y <= 0:
        new_y = 0
    window.geometry(f"+{new_x}+{new_y}")


def bind_move(widget: Widget, window: Tk = None):
    if window is None:
        from tkinter import _default_root
        window = _default_root
    widget.bind("<Button-1>", click)
    widget.bind("<B1-Motion>", lambda event: move(event, widget, window))


def tag_bind_move(widget: Widget, tag, window: Tk = None):
    if window is None:
        from tkinter import _default_root
        window = _default_root
    widget.tag_bind(tag, "<Button-1>", click)
    widget.tag_bind(tag, "<B1-Motion>", lambda event: move(event, widget, window))


if __name__ == '__main__':
    from tkadw import *

    root = AdwTMainWindow()
    root.geometry("500x340")
    root.overrideredirect(True)

    theme = AdwWin11Theme()
    root.theme(theme, "dark")

    menubar = AdwTMenuBar(root)
    menubar.show()
    bind_move(menubar, root)

    root.mainloop()