from .theme import AdwTheme


class AdwWin11Theme(AdwTheme):
    def __init__(self):
        self.theme = {
            "name": "Windows11",

            "light": {
                "window": {
                    "back": "#f4f4f4"
                },

                "button": {
                    "radius": 13,

                    "default": {
                        "back": "#fdfdfd",
                        "border": "#ededed",
                        "fore": "#202020",
                        "border_width": 1,
                    },

                    "hover": {
                        "back": "#f9f9f9",
                        "border": "#d5d5d5",
                        "fore": "#202020",
                        "border_width": 1,
                    },

                    "down": {
                        "back": "#fafafa",
                        "border": "#ebebeb",
                        "fore": "#202020",
                        "border_width": 1,
                    },
                },

                "circularbutton": {
                    "radius": 13,

                    "default": {
                        "back": "#fdfdfd",
                        "border": "#ededed",
                        "fore": "#202020",
                        "border_width": 1,
                    },

                    "hover": {
                        "back": "#f9f9f9",
                        "border": "#d5d5d5",
                        "fore": "#202020",
                        "border_width": 1,
                    },

                    "down": {
                        "back": "#fafafa",
                        "border": "#ebebeb",
                        "fore": "#202020",
                        "border_width": 1,
                    },
                },

                "entry": {
                    "radius": 13,

                    "default": {
                        "back": "#ffffff",
                        "border": "#e6e6e6",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#9c9c9c",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#ffffff",
                        "border": "#ebebeb",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#005fb8",
                        "bottomsheet_width": 2,
                    }
                },

                "frame": {
                    "radius": 15,
                    "back": "#fafafa",
                    "border": "#e7e7e7",
                    "border_width": 1,
                },

                "label": {
                    "fore": "#000000"
                },

                "menubar": {
                    "back": "#fdfdfd",
                    "border": "#ededed",
                },

                "separator": {
                    "fore": "#d0d0d0",
                    "border_width": 1,
                    "rounded": True
                },

                "sizegrip": {
                    "fore": "#ededed",
                },

                "text": {
                    "radius": 13,

                    "default": {
                        "back": "#ffffff",
                        "border": "#e6e6e6",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#9c9c9c",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#ffffff",
                        "border": "#ebebeb",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#005fb8",
                        "bottomsheet_width": 2,
                    }
                },

                "titlebar": {
                    "back": "#fdfdfd",
                    "border": "#ededed",
                    "fore": "#000000",
                    "title_anchor": "w",
                },

            },

            "dark": {
                "window": {
                    "back": "#202020"
                },

                "button": {
                    "radius": 13,

                    "default": {
                        "back": "#2a2a2a",
                        "border": "#313131",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },

                    "hover": {
                        "back": "#2f2f2f",
                        "border": "#313131",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },

                    "down": {
                        "back": "#232323",
                        "border": "#2c2c2c",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },
                },

                "circularbutton": {
                    "radius": 13,

                    "default": {
                        "back": "#2a2a2a",
                        "border": "#313131",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },

                    "hover": {
                        "back": "#2f2f2f",
                        "border": "#313131",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },

                    "down": {
                        "back": "#232323",
                        "border": "#2c2c2c",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },
                },

                "entry": {
                    "radius": 13,

                    "default": {
                        "back": "#2c2c2c",
                        "border": "#383838",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#686868",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#1c1c1c",
                        "border": "#2c2c2c",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#57c8ff",
                        "bottomsheet_width": 2,
                    }
                },

                "frame": {
                    "radius": 15,
                    "back": "#1c1c1c",
                    "border": "#2f2f2f",
                    "border_width": 1,
                },

                "label": {
                    "fore": "#ffffff"
                },

                "menubar": {
                    "back": "#2a2a2a",
                    "border": "#313131",
                },

                "separator": {
                    "fore": "#404040",
                    "border_width": 1,
                    "rounded": True
                },

                "sizegrip": {
                    "fore": "#313131",
                },

                "text": {
                    "radius": 13,

                    "default": {
                        "back": "#2c2c2c",
                        "border": "#383838",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#686868",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#1c1c1c",
                        "border": "#2c2c2c",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#57c8ff",
                        "bottomsheet_width": 2,
                    }
                },

                "titlebar": {
                    "back": "#2a2a2a",
                    "border": "#313131",
                    "fore": "#ffffff",
                    "title_anchor": "w",
                },

            }
        }

    def accent(self, color, darkcolor):
        self.configure("light", "entry", "bottomsheet", color, state="focus")
        self.configure("dark", "entry", "bottomsheet", darkcolor, state="focus")
        self.configure("light", "text", "bottomsheet", color, state="focus")
        self.configure("dark", "text", "bottomsheet", darkcolor, state="focus")
