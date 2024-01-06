from .frame import AdwFrame


class AdwWindowsMDI(AdwFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    from .window import AdwWindow

    def create_child_window(self, windowtype=AdwWindow, *args, **kwargs):
        _ = windowtype(*args, **kwargs)
        self.add_child_window(_)
        return _

    def add_child_window(self, window):
        from win32gui import SetParent, GetParent
        SetParent(GetParent(window.winfo_id()), GetParent(self.winfo_id()))
