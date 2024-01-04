from tkadw4.windows.canvas.frame import AdwDrawRoundFrame3
from tkadw4.windows.canvas.button import AdwDrawCircularButton



class AdwMDI(AdwDrawRoundFrame3):
    """
    多文档窗口
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mdichildren = []

    def create_child(self, x=10, y=10, width=150, height=150, closebutton=AdwDrawCircularButton, can_close: bool = True,
                     childframe=AdwDrawRoundFrame3, titlebarframe=AdwDrawRoundFrame3, content=AdwDrawRoundFrame3):
        """
        创建一个子窗口

        :return: AdwTFrame
        """
        child = childframe(self.frame)
        child.place(x=x, y=y, width=width, height=height)

        child.titlebar = titlebarframe(child.frame, height=34)
        child.titlebar.frame_border_width = 0
        child.titlebar.frame_border = child.frame_back
        child.closebutton = closebutton(child.titlebar.frame, text="✕", width=25, height=25)
        if can_close:  # 不推荐使用
            child.closebutton.configure(command=lambda: child.place_forget())
        child.closebutton.pack(anchor="ne", padx=2, pady=2)
        child.titlebar.row(fill="x", side="top", padx=2, pady=2)

        child.titlebar.frame.bind("<Button-1>", self._click, add="+")
        child.titlebar.frame.bind("<B1-Motion>", lambda event: self._move(event, child), add="+")

        child.content = content(child.frame, height=120)
        child.content.row(fill="both", expand="yes", padx=2, pady=2)

        self.mdichildren.append(child)

        return child.content, child

    def create_designer_child(self, x=10, y=10, width=150, height=150, closebutton=AdwDrawCircularButton, can_close: bool = True,
                              childframe=AdwDrawRoundFrame3, titlebarframe=AdwDrawRoundFrame3, content=AdwDrawRoundFrame3):
        from tkadw4.designer.designerframe import AdwDesignerFrame
        child = AdwDesignerFrame(self, childframe)
        child.place(x=x, y=y, width=width, height=height)

        child.titlebar = titlebarframe(child.widget, height=34)
        child.titlebar.frame_border_width = 0
        child.titlebar.frame_border = child.widget.frame_back
        child.closebutton = closebutton(child.titlebar.frame, text="✕", width=25, height=25)
        if can_close:  # 不推荐使用
            child.closebutton.configure(command=lambda: child.place_forget())
        child.closebutton.pack(anchor="ne", padx=2, pady=2)
        child.titlebar.pack(fill="x", side="top", padx=2, pady=2)

        child.titlebar.frame.bind("<Button-1>", self._click, add="+")
        child.titlebar.frame.bind("<Button-1>", lambda event: child.titlebar.frame.focus_set(), add="+")
        child.titlebar.frame.bind("<B1-Motion>", lambda event: self._move(event, child), add="+")

        child.content = content(child.widget, height=120)
        child.content.row(fill="both", expand="yes", padx=6, pady=6)

        self.mdichildren.append(child)

        return child.content, child

    def _click(self, event):
        self.x, self.y = event.x, event.y

    def _move(self, event, child):
        child.place(
            x=(event.x - self.x) + child.winfo_x(),
            y=(event.y - self.y) + child.winfo_y()
        )

    def palette(self, dict=None):
        super().palette(dict)
        if hasattr(self, "mdichildren"):
            for child in self.mdichildren:
                child.palette(dict)


if __name__ == '__main__':
    from tkadw4 import Adwite, set_default_theme, AdwTCircularButton, AdwTFrame, AdwTDesignerFrame

    set_default_theme("gtk", "light")

    root = Adwite()

    mdi = AdwMDI()
    mdiChild1 = mdi.create_child(childframe=AdwTFrame, titlebarframe=AdwTFrame, closebutton=AdwTCircularButton)
    mdiChild2 = mdi.create_designer_child(childframe=AdwTFrame, titlebarframe=AdwTFrame, closebutton=AdwTCircularButton)
    mdi.pack(fill="both", expand="yes", padx=10, pady=10)

    root.mainloop()
