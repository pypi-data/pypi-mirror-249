class WindowManager:
    def __init__(self, master=None):
        from .root import root
        self.master = root(master)

    def frameless(self, enable: bool):
        if enable:
            from sys import platform
            self.master.overrideredirect(True)
            if platform == "win32":
                try:
                    from win32gui import GetParent, GetWindowLong, SetWindowLong
                    from win32con import GWL_EXSTYLE, WS_EX_APPWINDOW, WS_EX_TOOLWINDOW
                    hwnd = GetParent(self.master.winfo_id())
                    style = GetWindowLong(hwnd, GWL_EXSTYLE)
                    style = style & ~WS_EX_TOOLWINDOW
                    style = style | WS_EX_APPWINDOW
                    SetWindowLong(hwnd, GWL_EXSTYLE, style)
                    self.master.after(1, lambda: self.master.withdraw())
                    self.master.after(2, lambda: self.master.deiconify())
                except:
                    self.master.wm_attributes("-topmost", True)
            else:
                self.master.wm_attributes("-topmost", True)
        elif not enable:
            self.master.overrideredirect(False)
        else:
            return self.master.overrideredirect()
