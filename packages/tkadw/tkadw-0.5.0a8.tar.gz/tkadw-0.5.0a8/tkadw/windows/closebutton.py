from .circularbutton import AdwCircularButton


class AdwCloseButton(AdwCircularButton):
    id = "closebutton"

    def __init__(self, *args, **kwargs):
        from .root import root
        super().__init__(*args, command=lambda: root(None).destroy(), **kwargs)
