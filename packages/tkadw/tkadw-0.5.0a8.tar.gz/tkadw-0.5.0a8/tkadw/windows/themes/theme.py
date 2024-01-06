from os.path import abspath, dirname
themepath = abspath(dirname(__file__))


class AdwTheme():

    path = None

    def __init__(self):
        from easydict import EasyDict as edict
        from .theme import themepath
        from os.path import join
        from json import loads
        self.fullpath = join(themepath, self.path)
        if self.path:
            self.theme = edict(
                loads(
                    open(self.fullpath, "r").read()
                )
            )

    def configure(self, mode: str, id: str, sheet, var, state=None):
        if state:
            self.theme[mode][id][state][sheet] = var
        else:
            self.theme[mode][id][sheet] = var

    def get(self):
        return self.theme
