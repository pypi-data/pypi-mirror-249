from tkadw4.windows.theme import AdwTFrame

__all__ = [
    "AdwDesigner",
]


class AdwDesigner(AdwTFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widgets = {}

        self.setup_project_panel()
        self.setup_widgets_panel()
        self.setup_designer_panel()

    def setup_project_panel(self):
        from tkadw4.windows.theme import AdwTListBox
        #from tkinterdnd2 import DND_ALL

        def delete(event):
            print(self.project_panel.select())
            if self.project_panel.select() is not None:
                _items = self.project_panel.cget("items")
                _items.remove(self.project_panel.select())
                self.widgets[self.project_panel.select()].destroy()
                self.project_panel.select(None)
                self.project_panel.update()

        def selection():
            try:
                self.after(100, self.widgets[self.project_panel.select()].widget.focus_set())
            except:
                pass

        self.project_panel = AdwTListBox(self.frame, width=130, item_selected=selection)
        self.project_panel.column(expand="no")
        self.project_panel.configure(item_selected=selection)
        self.project_panel.bind("<BackSpace>", delete)

    def setup_widgets_panel(self):
        from tkadw4.windows.theme import AdwTListBox
        #from tkinterdnd2 import DND_ALL

        self.widgets_panel = AdwTListBox(self.frame, items=["AdwTButton", "AdwTEntry", "AdwTText"], width=130)
        self.widgets_panel.bind("<Return>", lambda event: self.add_widget())

        self.widgets_panel.column(expand="no")

    def setup_designer_panel(self):
        from tkadw4.windows.theme import AdwTMDI
        self.designer_panel = AdwTMDI(self.frame)
        self.designer_window = self.designer_panel.create_designer_child(width=200, height=200)
        self.designer_panel.column()

    def add_widget(self):
        if self.widgets_panel.select() == "AdwTButton":
            from tkadw4.windows.theme import AdwTButton, AdwTDesignerFrame
            _ = AdwTDesignerFrame(self.designer_window[0], AdwTButton)
        elif self.widgets_panel.select() == "AdwTEntry":
            from tkadw4.windows.theme import AdwTEntry, AdwTDesignerFrame
            _ = AdwTDesignerFrame(self.designer_window[0], AdwTEntry)
        elif self.widgets_panel.select() == "AdwTText":
            from tkadw4.windows.theme import AdwTText, AdwTDesignerFrame
            _ = AdwTDesignerFrame(self.designer_window[0], AdwTText)
        _.place(x=20, y=40, width=100, height=40)
        _items = self.project_panel.cget("items")
        _items.append(_.winfo_id())
        self.project_panel.configure(items=_items)
        _.focus_set()
        self.project_panel.select(_.winfo_id())
        self.widgets[_.winfo_id()] = _


if __name__ == '__main__':
    from tkadw4 import *
    root = Adwite(default_theme="win11")
    root.geometry("650x360")
    designer = AdwDesigner()
    designer.row()
    root.mainloop()