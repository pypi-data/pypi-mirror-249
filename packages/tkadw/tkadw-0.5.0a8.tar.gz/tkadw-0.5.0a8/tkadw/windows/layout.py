from tkinterflow.tkinterflow import _flow, _flow_destroy


class Flow(object):
    mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


from tkinter import Widget


def put_configure(widget: Widget, x=0, y=0, width=0, height=0, top=None, bottom=None, left=None, right=None, *args,
                  **kwargs):
    def configure(evt):
        if top is not None:
            y = top
        if left is not None:
            x = left
        if right is not None:
            width = widget.master.winfo_width() - x - right
        if bottom is not None:
            height = widget.master.winfo_height() - y - bottom
        widget.place(x=x, y=y, width=width, height=height, *args, **kwargs)

    configure(None)
    return widget.master.bind("<Configure>", configure, add="+"), widget.bind("<Configure>", configure, add="+"), \
        {"in": widget.place_info()["in"], "x": x, "y": y, "width": width, "height": height, "top": top,
         "bottom": bottom, "left": left, "right": right}


def put_forget(widget: Widget, putid):
    """
最好请使用Adw.run()
    """
    widget.place_forget()
    widget.unbind("<Configure>", putid)


class AdwLayoutPut:
    def put_configure(self, *args, **kwargs):
        r = put_configure(self, *args, **kwargs)
        self.putid = r[0]
        self.putid2 = r[1]
        self.putinfo = r[2]

    put = put_configure

    def put_forget(self):
        return put_forget(self, self.putid), put_forget(self, self.putid2)

    def put_info(self):
        return self.putinfo


class AdwLayout(Flow, AdwLayoutPut):
    pass
