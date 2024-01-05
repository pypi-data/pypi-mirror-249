class AdwSimpleThemeBuilder(object):
    def __init__(self,
                 light="#f4f4f4",
                 dark="#202020",
                 primary_light="#005fb8",
                 primary_dark="#57c8ff",
                 border_light="#ededed",
                 border_dark="#2a2a2a",
                 default_light="#fdfdfd",
                 default_dark="#2a2a2a",
                 hover_light="#f9f9f9",
                 hover_dark="#2f2f2f",
                 down_light="#fafafa",
                 down_dark="#232323",
                 border_width=1,
                 bottom_sheet_width=1,
                 radius=12,
                 ):
        self.theme = {
            "light": {
                "window": {
                    "back": light
                },

                "button": {
                    "radius": radius,

                    "default": {
                        "back": default_light,
                        "border": border_light,
                        "fore": dark,
                        "border_width": border_width,
                    },

                    "active": {
                        "back": hover_light,
                        "border": border_light,
                        "fore": dark,
                        "border_width": border_width,
                    },

                    "pressed": {
                        "back": default_light,
                        "border": border_light,
                        "fore": dark,
                        "border_width": border_width,
                    },
                },

                "entry": {
                    "radius": radius,

                    "default": {
                        "back": default_light,
                        "border": border_light,
                        "fore": dark,
                        "border_width": border_width,

                        "bottomsheet": border_light,
                        "bottomsheet_width": bottom_sheet_width,
                    },

                    "focus": {
                        "back": down_light,
                        "border": border_light,
                        "fore": dark,
                        "border_width": border_width,

                        "bottomsheet": primary_light,
                        "bottomsheet_width": bottom_sheet_width + 1,
                    }
                },

                "label": {
                    "fore": dark,
                },

                "separator": {
                    "fore": dark,
                    "border_width": border_width,
                    "rounded": True
                },

                "text": {
                    "radius": radius,

                    "default": {
                        "back": default_light,
                        "border": border_light,
                        "fore": dark,
                        "border_width": border_width,

                        "bottomsheet": border_light,
                        "bottomsheet_width": bottom_sheet_width,
                    },

                    "focus": {
                        "back": down_light,
                        "border": border_light,
                        "fore": dark,
                        "border_width": border_width,

                        "bottomsheet": primary_light,
                        "bottomsheet_width": bottom_sheet_width + 1,
                    }
                },

            },
            "dark": {
                "window": {
                    "back": dark
                },

                "button": {
                    "radius": radius,

                    "default": {
                        "back": default_dark,
                        "border": border_dark,
                        "fore": light,
                        "border_width": border_width,
                    },

                    "active": {
                        "back": hover_dark,
                        "border": border_dark,
                        "fore": light,
                        "border_width": border_width,
                    },

                    "pressed": {
                        "back": default_dark,
                        "border": border_dark,
                        "fore": light,
                        "border_width": border_width,
                    },
                },

                "entry": {
                    "radius": radius,

                    "default": {
                        "back": default_dark,
                        "border": border_dark,
                        "fore": light,
                        "border_width": border_width,

                        "bottomsheet": border_dark,
                        "bottomsheet_width": bottom_sheet_width,
                    },

                    "focus": {
                        "back": down_dark,
                        "border": border_dark,
                        "fore": light,
                        "border_width": border_width,

                        "bottomsheet": primary_dark,
                        "bottomsheet_width": bottom_sheet_width + 1,
                    }
                },

                "label": {
                    "fore": light,
                },

                "separator": {
                    "fore": light,
                    "border_width": border_width,
                    "rounded": True
                },

                "text": {
                    "radius": radius,

                    "default": {
                        "back": default_dark,
                        "border": border_dark,
                        "fore": light,
                        "border_width": border_width,

                        "bottomsheet": border_dark,
                        "bottomsheet_width": bottom_sheet_width,
                    },

                    "focus": {
                        "back": down_dark,
                        "border": border_dark,
                        "fore": light,
                        "border_width": border_width,

                        "bottomsheet": primary_dark,
                        "bottomsheet_width": bottom_sheet_width + 1,
                    }
                },

            }
        }

    def configure(self, mode: str, id: str, sheet, var, state=None):
        if state:
            self.theme[mode][id][state][sheet] = var
        else:
            self.theme[mode][id][sheet] = var

    def get(self):
        return self.theme
