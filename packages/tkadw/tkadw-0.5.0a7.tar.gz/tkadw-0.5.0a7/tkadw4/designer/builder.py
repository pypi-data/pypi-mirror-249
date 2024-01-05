from tkinter import Tk, _get_default_root
from json import dumps, loads


class AdwBuilder(object):
    def __init__(self, data=None, data_of_json=None):
        _ = data
        if data_of_json is not None:
            _ = loads(data_of_json)
        if "adwite" in _:
            if "theme" in _["adwite"]:
                from tkadw4 import set_default_theme
                mode = "system"
                if "mode" in _["adwite"]:
                    mode = _["adwite"]["mode"]
                set_default_theme(_["adwite"]["theme"], mode)
        self.keys = {}
        if "widgets" in _:
            widgets = _["widgets"]
        elif "Widgets" in _:
            widgets = _["Widgets"]
        else:
            widgets = None
        if widgets is not None:
            for index in widgets:
                _name = index.split("::")[0]
                _type = index.split("::")[1]
                if _type == "Adwite":
                    from tkadw4.windows.theme import Adwite
                    type = Adwite
                elif _type == "Adw":
                    from tkadw4.windows.widgets.adw import Adw
                    type = Adw
                elif _type == "AdwTLabel":
                    from tkadw4.windows.theme import AdwTLabel
                    type = AdwTLabel

                if "master" in widgets[index]:
                    master = self.getkey(widgets[index]["master"])
                else:
                    master = None
                self.keys[_name] = type(master=master)
                if "title" in widgets[index]:
                    self.keys[_name].title(widgets[index]["title"])
                if "text" in widgets[index]:
                    self.keys[_name].configure(text=widgets[index]["text"])

    def getkey(self, key):
        return self.keys[key]


if __name__ == '__main__':
    from tkadw4 import Adwite

    builder = AdwBuilder(
        {
            "adwite": {
                "theme": "win11",
                "mode": "dark"
            },
            "Widgets": {
                "Root::Adwite": {
                    "title": "AdwBuilder"
                },
                "Label::AdwTLabel": {
                    "master": "Root",
                    "text": "AdwBuilder"
                }
            }
        }
    )
    root = builder.getkey("Root")
    label = builder.getkey("Label")
    label.pack(fill="both")
    root.update()
    root.mainloop()
