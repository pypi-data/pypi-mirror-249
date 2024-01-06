from tkinter import Event, Widget, Tk, Frame

x, y = 0, 0


def _click(event: Event):
    global x, y
    x, y = event.x, event.y


def _window_move(event: Event, widget: Widget, window: Tk):
    global x, y
    new_x = (event.x - x) + window.winfo_x()
    new_y = (event.y - y) + window.winfo_y()
    if new_y <= 0:
        new_y = 0
    window.geometry(f"+{new_x}+{new_y}")


def _widget_move(event: Event, widget: Widget):
    global x, y
    new_x = (event.x - x) + widget.winfo_x()
    new_y = (event.y - y) + widget.winfo_y()
    if new_y <= 0:
        new_y = 0
    widget.place(x=new_x, y=new_y)


def bind_window_move(widget: Widget, window: Tk = None):
    from .root import root
    window = root(window)
    widget.bind("<Button-1>", _click)
    widget.bind("<B1-Motion>", lambda event: _window_move(event, widget, window))


def tag_bind_window_move(widget: Widget, tag, window: Tk = None):
    from .root import root
    window = root(window)
    widget.tag_bind(tag, "<Button-1>", _click)
    widget.tag_bind(tag, "<B1-Motion>", lambda event: _window_move(event, widget, window))


def bind_widget_move(widget: Widget):
    widget.bind("<Button-1>", _click)
    widget.bind("<B1-Motion>", lambda event: _widget_move(event, widget))


def tag_bind_widget_move(widget: Widget, tag):
    widget.tag_bind(tag, "<Button-1>", _click)
    widget.tag_bind(tag, "<B1-Motion>", lambda event: _widget_move(event, widget))


if __name__ == '__main__':
    from tkadw import *

    root = AdwTMainWindow()
    root.geometry("500x340")
    root.overrideredirect(True)

    theme = AdwWin11Theme()
    root.theme(theme, "dark")

    button = AdwTDivider()
    bind_widget_move(button)
    button.place(x=50, y=50)

    menubar = create_root_themed_menubar()
    bind_window_move(menubar, root)

    root.mainloop()
