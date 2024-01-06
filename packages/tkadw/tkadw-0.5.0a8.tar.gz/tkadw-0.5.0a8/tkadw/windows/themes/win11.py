from .theme import AdwTheme


class AdwWin11Theme(AdwTheme):

    path = "win11.json"

    def __init__(self, accent: list = None):
        super().__init__()
        if accent:
            self.accent(accent[0], accent[1])

    def accent(self, color, darkcolor):
        self.theme.light.entry.focus.bottomsheet = color
        self.theme.dark.entry.focus.bottomsheet = darkcolor
        self.theme.light.text.focus.bottomsheet = color
        self.theme.dark.text.focus.bottomsheet = darkcolor

