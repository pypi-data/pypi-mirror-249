from .theme import AdwTheme


class AdwAntTheme(AdwTheme):

    path = "ant.json"

    def __init__(self):
        super().__init__()