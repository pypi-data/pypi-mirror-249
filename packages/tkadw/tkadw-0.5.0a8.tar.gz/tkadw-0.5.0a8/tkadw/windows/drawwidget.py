from .drawengine import AdwDrawEngine


class AdwDrawWidget(AdwDrawEngine):
    id = "draw-widget"

    def __init__(self, *args, width=80, height=30, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.bind("<Configure>", self._event_configure, add="+")
        self.bind("<Enter>", self._event_enter, add="+")
        self.bind("<Leave>", self._event_leave, add="+")
        self.bind("<ButtonPress>", self._buttonpress, add="+")
        self.bind("<ButtonRelease>", self._buttonrelease, add="+")
        self.bind("<FocusIn>", self._event_focus_in, add="+")
        self.bind("<FocusOut>", self._event_focus_out, add="+")

        self._is_enter = False
        self._is_leave = True
        self._is_button = False
        self._is_focus = False

    def _buttonpress(self, event=None):
        self._is_button = True
        self.update()

    def _buttonrelease(self, event=None):
        if self._is_enter:
            self.event_generate("<<Click>>")
            try:
                self.focus_set()
            except:
                pass
        self._is_button = False
        self.update()

    def _event_configure(self, event=None):
        self.update()

    def _draw(self, event=None):
        """
        --请在此处绘制组件--
        """
        try:
            self.delete("all")
        except:
            pass

    def _event_enter(self, event=None):
        self._is_enter = True
        self._is_leave = False
        self.update()

    def _event_leave(self, event=None):
        self._is_enter = False
        self._is_leave = True
        self.update()

    def _event_focus_in(self, event=None):
        self._is_focus = True
        self.update()

    def _event_focus_out(self, event=None):
        self._is_focus = False
        self.update()

    def _other(self, event=None):
        try:
            self.configure(background=self.master.cget("background"))
        except:
            pass

    def default_palette(self):
        pass

    def palette(self, palette: dict):
        for child in self.winfo_children():
            if hasattr(child, "palette"):
                child.palette(palette)
                child.update()

    def update(self):
        super().update()
        self._other()
        self._draw()
