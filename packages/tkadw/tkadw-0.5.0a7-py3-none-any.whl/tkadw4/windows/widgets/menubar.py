from tkadw4 import AdwDrawFrame


class AdwMenuBar(AdwDrawFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self):
        self.row(expand="no")
