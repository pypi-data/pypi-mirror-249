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
