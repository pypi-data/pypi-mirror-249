class AdwTheme():
    def __init__(self):
        self.theme = {}

    def configure(self, mode: str, id: str, sheet, var, state=None):
        if state:
            self.theme[mode][id][state][sheet] = var
        else:
            self.theme[mode][id][sheet] = var

    def get(self):
        return self.theme
