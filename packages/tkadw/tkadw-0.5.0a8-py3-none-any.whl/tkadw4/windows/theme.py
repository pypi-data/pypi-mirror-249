import typing

win11_theme = {
    "light": {
        "window": {
            "back": "#f4f4f4"
        },

        "label": {
            "back": "transparent",
            "text_back": "#000000",
        },

        "button": {
            "radius": 13,
            "back": "#fdfdfd",
            "border": "#ededed",
            "text_back": "#202020",
            "border_width": 1,

            "active": {
                "back": "#f9f9f9",
                "border": "#d5d5d5",
                "text_back": "#202020",
                "border_width": 1,
            },

            "pressed": {
                "back": "#fafafa",
                "border": "#ebebeb",
                "text_back": "#202020",
                "border_width": 1,
            },
        },

        "circular_button": {
            "back": "#fdfdfd",
            "border": "#ededed",
            "text_back": "#202020",
            "border_width": 1,

            "active": {
                "back": "#f9f9f9",
                "border": "#d5d5d5",
                "text_back": "#202020",
                "border_width": 1,
            },

            "pressed": {
                "back": "#fafafa",
                "border": "#ebebeb",
                "text_back": "#202020",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 15,
            "back": "#fafafa",
            "border": "#e7e7e7",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 13,
            "padding": (8, 8),

            "back": "#ffffff",
            "border": "#e6e6e6",
            "text_back": "#18191c",
            "border_width": 1,

            "bottom_line": "#9c9c9c",
            "bottom_width": 1,

            "focusin": {
                "back": "#ffffff",
                "border": "#ebebeb",
                "text_back": "#18191c",
                "border_width": 1,

                "bottom_line": "#005fb8",
                "bottom_width": 2,
            }
        },

        "text": {
            "radius": 13,
            "padding": (8, 8),

            "back": "#ffffff",
            "border": "#e6e6e6",
            "text_back": "#18191c",
            "border_width": 1,

            "bottom_line": "#9c9c9c",
            "bottom_width": 1,

            "focusin": {
                "back": "#ffffff",
                "border": "#ebebeb",
                "text_back": "#18191c",
                "border_width": 1,

                "bottom_line": "#005fb8",
                "bottom_width": 2,
            }
        },

        "separator": {
            "back": "#d0d0d0",
            "border_width": 1,

            "rounded": True
        },

        "designer_frame": {
            "border": "black",
            "grip": "black"
        },

        "listbox": {
            "back": "#fafafa",
            "border": "#e7e7e7",
            "border_width": 1,
            "padding": 0,
            "radius": 6,

            "item_back": "#fafafa",
            "item_border": "#fafafa",
            "item_text": "#000000",

            "item_radius": 10,
            "item_height": 36,
            "item_padding": 1,

            "active": {
                "item_back": "#005fb8",
                "item_border": "#005fb8",
                "item_text": "#ffffff",
            },
        }
    },
    "dark": {
        "window": {
            "back": "#202020"
        },

        "label": {
            "back": "transparent",
            "text_back": "#ffffff",
        },

        "button": {
            "radius": 13,
            "back": "#2a2a2a",
            "border": "#313131",
            "text_back": "#ebebeb",
            "border_width": 1,

            "active": {
                "back": "#2f2f2f",
                "border": "#313131",
                "text_back": "#ebebeb",
                "border_width": 1,
            },

            "pressed": {
                "back": "#232323",
                "border": "#2c2c2c",
                "text_back": "#ebebeb",
                "border_width": 1,
            },
        },

        "circular_button": {
            "back": "#2a2a2a",
            "border": "#313131",
            "text_back": "#ebebeb",
            "border_width": 1,

            "active": {
                "back": "#2f2f2f",
                "border": "#313131",
                "text_back": "#ebebeb",
                "border_width": 1,
            },

            "pressed": {
                "back": "#232323",
                "border": "#2c2c2c",
                "text_back": "#ebebeb",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 15,
            "back": "#1c1c1c",
            "border": "#2f2f2f",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 13,
            "padding": (8, 8),

            "back": "#2c2c2c",
            "border": "#383838",
            "text_back": "#e7e9eb",
            "border_width": 1,

            "bottom_line": "#686868",
            "bottom_width": 1,

            "focusin": {
                "back": "#1c1c1c",
                "border": "#2c2c2c",
                "text_back": "#e7e9eb",
                "border_width": 1,

                "bottom_line": "#57c8ff",
                "bottom_width": 2,
            }
        },

        "text": {
            "radius": 13,
            "padding": (8, 8),

            "back": "#2c2c2c",
            "border": "#383838",
            "text_back": "#e7e9eb",
            "border_width": 1,

            "bottom_line": "#686868",
            "bottom_width": 1,

            "focusin": {
                "back": "#1c1c1c",
                "border": "#2c2c2c",
                "text_back": "#e7e9eb",
                "border_width": 1,

                "bottom_line": "#57c8ff",
                "bottom_width": 2,
            }
        },

        "separator": {
            "back": "#404040",
            "border_width": 1,

            "rounded": True
        },

        "designer_frame": {
            "border": "white",
            "grip": "white"
        },

        "listbox": {
            "back": "#1c1c1c",
            "border": "#2f2f2f",
            "border_width": 1,
            "padding": 0,
            "radius": 6,

            "item_back": "#1c1c1c",
            "item_border": "#1c1c1c",
            "item_text": "#ffffff",

            "item_radius": 10,
            "item_height": 36,
            "item_padding": 1,

            "active": {
                "item_back": "#57c8ff",
                "item_border": "#57c8ff",
                "item_text": "#000000",
            },
        }
    }
}

gtk_theme = {
    "light": {
        "window": {
            "back": "#ffffff"
        },

        "label": {
            "back": "transparent",
            "text_back": "#000000",
        },

        "button": {
            "radius": 11,
            "back": "#f6f5f4",
            "border": "#ccc6c1",
            "text_back": "#2e3436",
            "border_width": 1.3,

            "active": {
                "back": "#f8f8f7",
                "border": "#dad6d2",
                "text_back": "#2e3436",
                "border_width": 1.3,
            },

            "pressed": {
                "back": "#dad6d2",
                "border": "#dad6d2",
                "text_back": "#2e3436",
                "border_width": 1.3,
            },
        },

        "circular_button": {
            "back": "#f6f5f4",
            "border": "#ccc6c1",
            "text_back": "#2e3436",
            "border_width": 1.3,

            "active": {
                "back": "#f8f8f7",
                "border": "#dad6d2",
                "text_back": "#2e3436",
                "border_width": 1.3,
            },

            "pressed": {
                "back": "#dad6d2",
                "border": "#dad6d2",
                "text_back": "#2e3436",
                "border_width": 1.3,
            },
        },

        "frame": {
            "radius": 0,
            "back": "#f6f5f4",
            "border": "#d5d0cc",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 11,
            "padding": (5, 5),

            "back": "#ffffff",
            "border": "#cdc7c2",
            "text_back": "#000000",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#3584e4",
                "text_back": "#000000",
                "border_width": 1,

                "bottom_line": "#185fb4",
                "bottom_width": 0,
            }
        },

        "text": {
            "padding": (5, 5),

            "radius": 0,
            "back": "#ffffff",
            "border": "#cdc7c2",
            "text_back": "#000000",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#3584e4",
                "text_back": "#000000",
                "border_width": 1,

                "bottom_line": "#185fb4",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#d8d4d0",
            "border_width": 1,

            "rounded": True
        },

        "designer_frame": {
            "border": "black",
            "grip": "black"
        },

        "listbox": {
            "back": "#f6f5f4",
            "border": "#d5d0cc",
            "border_width": 1,
            "padding": 0,
            "radius": 0,

            "item_back": "#f6f5f4",
            "item_border": "#f6f5f4",
            "item_text": "#000000",

            "item_radius": 8,
            "item_height": 25,
            "item_padding": 1,

            "active": {
                "item_back": "#3584e4",
                "item_border": "#3584e4",
                "item_text": "#ffffff",
            },
        }
    },
    "dark": {
        "window": {
            "back": "#353535"
        },

        "label": {
            "back": "transparent",
            "text_back": "#ffffff",
        },

        "button": {
            "radius": 11,
            "back": "#353535",
            "border": "#1b1b1b",
            "text_back": "#eeeeec",
            "border_width": 1.3,

            "active": {
                "back": "#373737",
                "border": "#1b1b1b",
                "text_back": "#eeeeec",
                "border_width": 1.3,
            },

            "pressed": {
                "back": "#1e1e1e",
                "border": "#282828",
                "text_back": "#eeeeec",
                "border_width": 1.3,
            },
        },

        "circular_button": {
            "back": "#353535",
            "border": "#1b1b1b",
            "text_back": "#eeeeec",
            "border_width": 1.3,

            "active": {
                "back": "#373737",
                "border": "#1b1b1b",
                "text_back": "#eeeeec",
                "border_width": 1.3,
            },

            "pressed": {
                "back": "#1e1e1e",
                "border": "#282828",
                "text_back": "#eeeeec",
                "border_width": 1.3,
            },
        },

        "frame": {
            "radius": 0,
            "back": "#313131",
            "border": "#1b1b1b",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 11,
            "padding": (5, 5),

            "back": "#2d2d2d",
            "border": "#1f1f1f",
            "text_back": "#cccccc",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#2d2d2d",
                "border": "#3584e4",
                "text_back": "#ffffff",
                "border_width": 1,

                "bottom_line": "#3584e4",
                "bottom_width": 0,
            }
        },

        "text": {
            "padding": (5, 5),

            "radius": 0,
            "back": "#2d2d2d",
            "border": "#1f1f1f",
            "text_back": "#cccccc",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#2d2d2d",
                "border": "#3584e4",
                "text_back": "#ffffff",
                "border_width": 1,

                "bottom_line": "#3584e4",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#282828",
            "border_width": 1,

            "rounded": True
        },

        "designer_frame": {
            "border": "white",
            "grip": "white"
        },

        "listbox": {
            "back": "#313131",
            "border": "#1b1b1b",
            "border_width": 1,
            "padding": 0,
            "radius": 0,

            "item_back": "#313131",
            "item_border": "#313131",
            "item_text": "#ffffff",

            "item_radius": 8,
            "item_height": 25,
            "item_padding": 1,

            "active": {
                "item_back": "#3584e4",
                "item_border": "#3584e4",
                "item_text": "#000000",
            },
        },
    }

}

bilibili_theme = {
    "light": {
        "window": {
            "back": "#ffffff"
        },

        "label": {
            "back": "transparent",
            "text_back": "#000000",
        },

        "button": {
            "radius": 16,
            "back": "#ffffff",
            "border": "#e3e5e7",
            "text_back": "#18191c",
            "border_width": 1,

            "active": {
                "back": "#e3e5e7",
                "border": "#e3e5e7",
                "text_back": "#18191c",
                "border_width": 1,
            },

            "pressed": {
                "back": "#eceff0",
                "border": "#e3e5e7",
                "text_back": "#6d7479",
                "border_width": 1,
            },
        },

        "circular_button": {
            "back": "#ffffff",
            "border": "#e3e5e7",
            "text_back": "#18191c",
            "border_width": 1,

            "active": {
                "back": "#e3e5e7",
                "border": "#e3e5e7",
                "text_back": "#18191c",
                "border_width": 1,
            },

            "pressed": {
                "back": "#eceff0",
                "border": "#e3e5e7",
                "text_back": "#6d7479",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 18,
            "back": "#f6f7f8",
            "border": "#f1f2f3",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 16,
            "padding": (8, 8),

            "back": "#ffffff",
            "border": "#e3e5e7",
            "text_back": "#18191c",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#ff6699",
                "text_back": "#18191c",
                "border_width": 1,

                "bottom_line": "#185fb4",
                "bottom_width": 0,
            }
        },

        "text": {
            "radius": 16,
            "padding": (8, 8),

            "back": "#ffffff",
            "border": "#e3e5e7",
            "text_back": "#18191c",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#ff6699",
                "text_back": "#18191c",
                "border_width": 1,

                "bottom_line": "#185fb4",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#f1f2f3",
            "border_width": 1,

            "rounded": True
        },

        "designer_frame": {
            "border": "#ff6699",
            "grip": "#ff6699"
        },

        "listbox": {
            "back": "#f6f7f8",
            "border": "#f1f2f3",
            "border_width": 1,
            "padding": 0,
            "radius": 18,

            "item_back": "#f6f7f8",
            "item_border": "#f6f7f8",
            "item_text": "#000000",

            "item_radius": 14,
            "item_height": 40,
            "item_padding": 1,

            "active": {
                "item_back": "#d44e7d",
                "item_border": "#d44e7d",
                "item_text": "#ffffff",
            },
        }, },

    "dark": {
        "window": {
            "back": "#17181a"
        },

        "label": {
            "back": "transparent",
            "text_back": "#ffffff",
        },

        "button": {
            "radius": 16,
            "back": "#242628",
            "border": "#2f3134",
            "text_back": "#dcdee0",
            "border_width": 1,

            "active": {
                "back": "#2f3134",
                "border": "#2f3134",
                "text_back": "#dcdee0",
                "border_width": 1,
            },

            "pressed": {
                "back": "#26282a",
                "border": "#2f3134",
                "text_back": "#a9abad",
                "border_width": 1,
            },
        },

        "circular_button": {
            "radius": 16,
            "back": "#242628",
            "border": "#2f3134",
            "text_back": "#dcdee0",
            "border_width": 1,

            "active": {
                "back": "#2f3134",
                "border": "#2f3134",
                "text_back": "#dcdee0",
                "border_width": 1,
            },

            "pressed": {
                "back": "#26282a",
                "border": "#2f3134",
                "text_back": "#a9abad",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 18,
            "back": "#1e2022",
            "border": "#232527",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 16,
            "padding": (8, 8),

            "back": "#17181a",
            "border": "#2f3134",
            "text_back": "#e7e9eb",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#17181a",
                "border": "#d44e7d",
                "text_back": "#e7e9eb",
                "border_width": 1,

                "bottom_line": "#d44e7d",
                "bottom_width": 0,
            }
        },

        "text": {
            "radius": 16,
            "padding": (8, 8),

            "back": "#17181a",
            "border": "#2f3134",
            "text_back": "#e7e9eb",
            "border_width": 1,

            "bottom_line": "#eaeaea",
            "bottom_width": 0,

            "focusin": {
                "back": "#17181a",
                "border": "#d44e7d",
                "text_back": "#e7e9eb",
                "border_width": 1,

                "bottom_line": "#d44e7d",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#232527",
            "border_width": 1,

            "rounded": True
        },

        "designer_frame": {
            "border": "#ff6699",
            "grip": "#ff6699"
        },

        "listbox": {
            "back": "#1e2022",
            "border": "#232527",
            "border_width": 1,
            "padding": 0,
            "radius": 18,

            "item_back": "#1e2022",
            "item_border": "#1e2022",
            "item_text": "#ffffff",

            "item_radius": 14,
            "item_height": 40,
            "item_padding": 1,

            "active": {
                "item_back": "#d44e7d",
                "item_border": "#d44e7d",
                "item_text": "#000000",
            },
        },
    }
}

metro_theme = {
    "light": {
        "window": {
            "back": "#ffffff"
        },

        "label": {
            "back": "transparent",
            "text_back": "#000000",
        },

        "button": {
            "radius": 0,
            "back": "#eeeeee",
            "border": "#cccccc",
            "text_back": "#000000",
            "border_width": 1,

            "active": {
                "back": "#666666",
                "border": "#666666",
                "text_back": "#ffffff",
                "border_width": 1,
            },

            "pressed": {
                "back": "#333333",
                "border": "#333333",
                "text_back": "#ffffff",
                "border_width": 1,
            },
        },

        "circular_button": {
            "back": "#eeeeee",
            "border": "#cccccc",
            "text_back": "#000000",
            "border_width": 1,

            "active": {
                "back": "#666666",
                "border": "#666666",
                "text_back": "#ffffff",
                "border_width": 1,
            },

            "pressed": {
                "back": "#333333",
                "border": "#333333",
                "text_back": "#ffffff",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 0,
            "back": "#ffffff",
            "border": "#bfbfbf",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 0,
            "padding": (3, 3),

            "back": "#ffffff",
            "border": "#999999",
            "text_back": "#000000",
            "border_width": 1,

            "bottom_line": "#ffffff",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#00aedb",
                "text_back": "#000000",
                "border_width": 1,

                "bottom_line": "#ffffff",
                "bottom_width": 0,
            }
        },

        "text": {
            "radius": 0,
            "padding": (3, 3),

            "back": "#ffffff",
            "border": "#999999",
            "text_back": "#000000",
            "border_width": 1,

            "bottom_line": "#ffffff",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#00aedb",
                "text_back": "#000000",
                "border_width": 1,

                "bottom_line": "#ffffff",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#999999",
            "border_width": 1,

            "rounded": True
        },

        "designer_frame": {
            "border": "black",
            "grip": "black"
        },

        "listbox": {
            "back": "#ffffff",
            "border": "#bfbfbf",
            "border_width": 1,
            "padding": 0,
            "radius": 0,

            "item_back": "#ffffff",
            "item_border": "#ffffff",
            "item_text": "#000000",

            "item_radius": 8,
            "item_height": 35,
            "item_padding": 1,

            "active": {
                "item_back": "#666666",
                "item_border": "#666666",
                "item_text": "#ffffff",
            },
        },
    },
    "dark": {
        "window": {
            "back": "#111111"
        },

        "label": {
            "back": "transparent",
            "text_back": "#ffffff",
        },

        "button": {
            "radius": 0,
            "back": "#222222",
            "border": "#444444",
            "text_back": "#ffffff",
            "border_width": 1,

            "active": {
                "back": "#aaaaaa",
                "border": "#aaaaaa",
                "text_back": "#000000",
                "border_width": 1,
            },

            "pressed": {
                "back": "#eeeeee",
                "border": "#eeeeee",
                "text_back": "#000000",
                "border_width": 1,
            },
        },

        "circular_button": {
            "back": "#222222",
            "border": "#444444",
            "text_back": "#ffffff",
            "border_width": 1,

            "active": {
                "back": "#aaaaaa",
                "border": "#aaaaaa",
                "text_back": "#000000",
                "border_width": 1,
            },

            "pressed": {
                "back": "#eeeeee",
                "border": "#eeeeee",
                "text_back": "#000000",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 0,
            "back": "#111111",
            "border": "#373737",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 0,
            "padding": (3, 3),

            "back": "#111111",
            "border": "#999999",
            "text_back": "#ffffff",
            "border_width": 1,

            "bottom_line": "#000000",
            "bottom_width": 0,

            "focusin": {
                "back": "#111111",
                "border": "#00aedb",
                "text_back": "#ffffff",
                "border_width": 1,

                "bottom_line": "#000000",
                "bottom_width": 0,
            }
        },

        "text": {
            "radius": 0,
            "padding": (3, 3),

            "back": "#111111",
            "border": "#999999",
            "text_back": "#ffffff",
            "border_width": 1,

            "bottom_line": "#000000",
            "bottom_width": 0,

            "focusin": {
                "back": "#111111",
                "border": "#00aedb",
                "text_back": "#ffffff",
                "border_width": 1,

                "bottom_line": "#000000",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#999999",
            "border_width": 1,

            "rounded": False
        },

        "designer_frame": {
            "border": "white",
            "grip": "white"
        },

        "listbox": {
            "back": "#111111",
            "border": "#373737",
            "border_width": 1,
            "padding": 0,
            "radius": 0,

            "item_back": "#111111",
            "item_border": "#111111",
            "item_text": "#ffffff",

            "item_radius": 8,
            "item_height": 35,
            "item_padding": 1,

            "active": {
                "item_back": "#aaaaaa",
                "item_border": "#aaaaaa",
                "item_text": "#000000",
            },
        },
    }
}

pypi_org_theme = {
    "light": {
        "window": {
            "back": "#ffffff"
        },

        "label": {
            "back": "transparent",
            "text_back": "#000000",
        },

        "button": {
            "radius": 8,
            "back": "#006dad",
            "border": "#006dad",
            "text_back": "#ffffff",
            "border_width": 1,

            "active": {
                "back": "#00507f",
                "border": "#00507f",
                "text_back": "#ffffff",
                "border_width": 1,
            },

            "pressed": {
                "back": "#00507f",
                "border": "#ffffff",
                "text_back": "#ffffff",
                "border_width": 1,
            },
        },

        "circular_button": {
            "back": "#006dad",
            "border": "#006dad",
            "text_back": "#ffffff",
            "border_width": 1,

            "active": {
                "back": "#00507f",
                "border": "#00507f",
                "text_back": "#ffffff",
                "border_width": 1,
            },

            "pressed": {
                "back": "#00507f",
                "border": "#ffffff",
                "text_back": "#ffffff",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 0,
            "back": "#ececec",
            "border": "#d3d3d3",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 8,
            "padding": (5, 5),

            "back": "#ffffff",
            "border": "#949494",
            "text_back": "#464646",
            "border_width": 1,

            "bottom_line": "#ffffff",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#006dad",
                "text_back": "#464646",
                "border_width": 3,

                "bottom_line": "#ffffff",
                "bottom_width": 0,
            }
        },

        "text": {
            "radius": 8,
            "padding": (8, 8),

            "back": "#ffffff",
            "border": "#949494",
            "text_back": "#464646",
            "border_width": 1,

            "bottom_line": "#ffffff",
            "bottom_width": 0,

            "focusin": {
                "back": "#ffffff",
                "border": "#006dad",
                "text_back": "#464646",
                "border_width": 3,

                "bottom_line": "#ffffff",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#d3d3d3",
            "border_width": 1,

            "rounded": False
        },

        "designer_frame": {
            "border": "#006dad",
            "grip": "#006dad"
        },

        "listbox": {
            "back": "#ececec",
            "border": "#d3d3d3",
            "border_width": 1,
            "padding": 0,
            "radius": 0,

            "item_back": "#ececec",
            "item_border": "#ececec",
            "item_text": "#000000",

            "item_radius": 0,
            "item_height": 35,
            "item_padding": 0,

            "active": {
                "item_back": "#00507f",
                "item_border": "#00507f",
                "item_text": "#ffffff",
            },
    },
    },

    "dark": {
        "window": {
            "back": "#000002"
        },

        "label": {
            "back": "transparent",
            "text_back": "#ffffff",
        },

        "button": {
            "radius": 8,
            "back": "#00569f",
            "border": "#00569f",
            "text_back": "#ffffff",
            "border_width": 1,

            "active": {
                "back": "#00356c",
                "border": "#00356c",
                "text_back": "#ffffff",
                "border_width": 1,
            },

            "pressed": {
                "back": "#00356c",
                "border": "#000000",
                "text_back": "#ffffff",
                "border_width": 1,
            },
        },

        "circular_button": {
            "back": "#00569f",
            "border": "#00569f",
            "text_back": "#ffffff",
            "border_width": 1,

            "active": {
                "back": "#00356c",
                "border": "#00356c",
                "text_back": "#ffffff",
                "border_width": 1,
            },

            "pressed": {
                "back": "#00356c",
                "border": "#000000",
                "text_back": "#ffffff",
                "border_width": 1,
            },
        },

        "frame": {
            "radius": 0,
            "back": "#0c1012",
            "border": "#30373b",
            "border_width": 1,
            "padding": 0
        },

        "entry": {
            "radius": 8,
            "padding": (5, 5),

            "back": "#000000",
            "border": "#1e2427",
            "text_back": "#d1deca",
            "border_width": 1,

            "bottom_line": "#ffffff",
            "bottom_width": 0,

            "focusin": {
                "back": "#000000",
                "border": "#004d8f",
                "text_back": "#d1deca",
                "border_width": 3,

                "bottom_line": "#ffffff",
                "bottom_width": 0,
            }
        },

        "text": {
            "radius": 8,
            "padding": (5, 5),

            "back": "#000000",
            "border": "#1e2427",
            "text_back": "#d1deca",
            "border_width": 1,

            "bottom_line": "#ffffff",
            "bottom_width": 0,

            "focusin": {
                "back": "#000000",
                "border": "#004d8f",
                "text_back": "#d1deca",
                "border_width": 3,

                "bottom_line": "#ffffff",
                "bottom_width": 0,
            }
        },

        "separator": {
            "back": "#30373b",
            "border_width": 1,

            "rounded": False
        },

        "designer_frame": {
            "border": "#00569f",
            "grip": "#00569f"
        },

        "listbox": {
            "back": "#0c1012",
            "border": "#30373b",
            "border_width": 1,
            "padding": 0,
            "radius": 0,

            "item_back": "#0c1012",
            "item_border": "#0c1012",
            "item_text": "#ffffff",

            "item_radius": 0,
            "item_height": 35,
            "item_padding": 0,

            "active": {
                "item_back": "#00356c",
                "item_border": "#00356c",
                "item_text": "#000000",
            },
        },
    }
}


def _set_theme_mode(mode):
    from os import environ
    environ["tkAdwite.ThemeMode"] = mode


def set_theme_mode(mode="system"):
    if mode == "system":
        try:
            from darkdetect import isDark
            if isDark():
                _set_theme_mode("dark")
            else:
                _set_theme_mode("light")
        except ModuleNotFoundError:
            pass
    else:
        _set_theme_mode(mode)


def get_theme_mode():
    from os import environ
    if "tkAdwite.ThemeMode" in environ:
        return environ["tkAdwite.ThemeMode"]
    else:
        return "light"


def get_default_theme():
    from os import environ
    from json import loads
    try:
        return loads(environ["tkAdwite.DefaultTheme"])
    except KeyError:
        return None


def _set_default_theme(theme):
    from os import environ
    from json import dumps
    environ["tkAdwite.DefaultTheme"] = dumps(theme)


def set_default_theme(theme, mode="system"):
    if theme == "win11" or theme == "windows11" or theme == "Windows11" or theme == "Win11":
        _set_default_theme(win11_theme)
    elif theme == "gtk" or theme == "Gtk":
        _set_default_theme(gtk_theme)
    elif theme == "bilibili" or theme == "BiliBili":
        _set_default_theme(bilibili_theme)
    elif theme == "metro" or theme == "Metro":
        _set_default_theme(metro_theme)
    elif theme == "pypi" or theme == "Pypi":
        _set_default_theme(pypi_org_theme)
    else:
        _set_default_theme(theme)


set_default_theme("win11")

from tkadw4.windows.widgets.adw import Adw


def check_system_toggle_theme(callable: typing.Callable[[str], None]) -> None:
    try:
        import threading
        import darkdetect
    except ModuleNotFoundError:
        pass
    else:
        t = threading.Thread(target=darkdetect.listener, args=(callable,))
        t.daemon = True
        t.start()


class Adwite(Adw):
    def __init__(self, default_theme="win11", default_theme_mode="system", *args, **kwargs):
        super().__init__(*args, **kwargs)
        check_system_toggle_theme(self.system_switch_theme)
        self.set_default_theme_mode(default_theme_mode)
        self.set_default_theme(default_theme)

    def system_switch_theme(self, theme):
        self.event_generate("<<SystemThemeSwitch>>", data=theme)

    def get_system_theme(self) -> str:
        try:
            from darkdetect import theme
        except ModuleNotFoundError:
            pass
        else:
            return theme()

    def get_json(self):
        from json import dumps
        return dumps(
            {
                "root": {
                    "type": type(self).__name__,
                    "title": self.title()
                }
            }
        )

    def set_default_theme(self, theme, _mode="auto"):
        """
        win11、basic、metro、bilibili、gtk
        """
        set_default_theme(theme, _mode)
        for widget in self.winfo_children():
            if hasattr(widget, "palette"):
                widget.palette(get_default_theme())
                widget.update()
                if hasattr(widget, "frame"):
                    for widgetf in widget.frame.winfo_children():
                        if hasattr(widgetf, "palette"):
                            widgetf.palette(get_default_theme())
                            widgetf.update()
        self.palette(get_default_theme()[get_theme_mode()])

        from sys import platform
        """
        if platform == "win32":
            from sys import platform
            from ctypes import windll, byref, sizeof, c_int
            from ctypes.wintypes import RGB
            color = self.winfo_rgb(self.cget("bg"))
            windll.dwmapi.DwmSetWindowAttribute(windll.user32.GetParent(self.winfo_id()), 35,
                                                byref(c_int(RGB(color[0], color[1], color[2]))),
                                                sizeof(c_int))
        """

    def set_default_theme_mode(self, mode):
        set_theme_mode(mode)
        for widget in self.winfo_children():
            if hasattr(widget, "palette"):
                widget.update()
                widget.palette(get_default_theme())
            if hasattr(widget, "frame"):
                for widgetf in widget.frame.winfo_children():
                    if hasattr(widgetf, "palette"):
                        widgetf.update()
                        widgetf.palette(get_default_theme())
        self.palette(get_default_theme()[get_theme_mode()])

    def default_palette(self):
        self.palette(get_default_theme()[get_theme_mode()])


from tkadw4.windows.widgets.toplevel import AdwToplevel


class Adwitew(Adwite, AdwToplevel):
    pass


class AdwThemed(object):
    def default_palette(self):
        self.palette(get_default_theme()[get_theme_mode()])

    def palette(self, *args, **kwargs):
        super().palette(get_default_theme()[get_theme_mode()])
        for child in self.winfo_children():
            if hasattr(child, "palette"):
                child.palette(get_default_theme()[get_theme_mode()])
        if hasattr(self, "frame"):
            for child in self.frame.winfo_children():
                if hasattr(child, "palette"):
                    child.palette(get_default_theme()[get_theme_mode()])


from tkadw4.windows.widgets import AdwLabel


class AdwTLabel(AdwThemed, AdwLabel):
    pass


from tkadw4.windows.canvas.button import AdwDrawRoundButton3


class AdwTButton(AdwThemed, AdwDrawRoundButton3):
    def win11_accent_dark(self):
        self.palette(
            {
                "button": {
                    "radius": 13,
                    "back": "#57c8ff",
                    "border": "#64cdff",
                    "text_back": "#1c1c1c",
                    "border_width": 1,

                    "active": {
                        "back": "#51b7eb",
                        "border": "#5fbced",
                        "text_back": "#1c1c1c",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#4ba6d5",
                        "border": "#59aed9",
                        "text_back": "#1c1c1c",
                        "border_width": 1,
                    },
                }
            }
        )

    def win11_accent_light(self):
        self.palette(
            {
                "button": {
                    "radius": 13,
                    "back": "#0560b6",
                    "border": "#1a6cba",
                    "text_back": "#ebebeb",
                    "border_width": 1,

                    "active": {
                        "back": "#1e6fbc",
                        "border": "#307bc2",
                        "text_back": "#ebebeb",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#327ec5",
                        "border": "#4288ca",
                        "text_back": "#ebebeb",
                        "border_width": 1,
                    },
                }
            }
        )


from tkadw4.windows.canvas.button import AdwDrawCircularButton


class AdwTCircularButton(AdwThemed, AdwDrawCircularButton):
    pass


from tkadw4.windows.canvas.entry import AdwDrawRoundEntry3


class AdwTEntry(AdwThemed, AdwDrawRoundEntry3):
    pass


from tkadw4.designer.designerframe import AdwDesignerFrame


class AdwTDesignerFrame(AdwThemed, AdwDesignerFrame):
    pass


from tkadw4.windows.canvas.textbox import AdwDrawRoundText3


class AdwTText(AdwThemed, AdwDrawRoundText3):
    pass


from tkadw4.windows.canvas.frame import AdwDrawRoundFrame3


class AdwTFrame(AdwThemed, AdwDrawRoundFrame3):
    pass


from tkadw4.windows.widgets.listbox import AdwRoundListBox3


class AdwTListBox(AdwThemed, AdwRoundListBox3):
    pass


from tkadw4.windows.canvas.separator import AdwDrawSeparator


class AdwTSeparator(AdwThemed, AdwDrawSeparator):
    pass


class AdwTStack(AdwTFrame):
    def __init__(self, *args, **kwargs):
        """
        用于切换不同的界面
        """
        super().__init__(*args, **kwargs)
        self._pages = {}

    def add_page(self, page: AdwTFrame, id: int = 0):
        """
        添加页面

        :param page: 页面组件
        :param id: 组件ID
        """
        self._pages[id] = page

    def show_page(self, id: int):
        """
        显示页面，会将其他页面隐藏

        :param id: 被显示的页面ID
        """
        self._pages[id].pack(fill="both", expand="yes")
        for item in self._pages.keys():
            if not item == id:
                self.hide_page(item)

    def hide_page(self, id: int):
        """
        内置函数，最好不要使用，因为几乎没有什么用
        """
        self._pages[id].pack_forget()

    def get_page(self, id: int):
        """
        获取页面

        :param id: 所要获取的页面ID
        """
        return self._pages[id]

    def get_pages(self):
        """
        获取所有页面
        """
        return self._pages


from tkadw4.windows.widgets.mdi import AdwMDI


class AdwTMDI(AdwThemed, AdwMDI):
    def create_child(self, x=10, y=10, width=150, height=150, can_close: bool = True, content=AdwTFrame,
                     closebutton=AdwTCircularButton, childframe=AdwTFrame, titlebarframe=AdwTFrame
                     ):
        return super().create_child(
            x=x, y=y, width=width, height=height, can_close=can_close, content=content,
            closebutton=closebutton, childframe=childframe, titlebarframe=titlebarframe
        )

    def create_designer_child(self, x=10, y=10, width=150, height=150, can_close: bool = True, content=AdwTFrame,
                              closebutton=AdwTCircularButton, childframe=AdwTFrame, titlebarframe=AdwTFrame
                              ):
        return super().create_designer_child(
            x=x, y=y, width=width, height=height, can_close=can_close, content=content,
            closebutton=closebutton, childframe=childframe, titlebarframe=titlebarframe
        )


class AdwTTabs(AdwTFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tab_panel = AdwTListBox(self.frame, item_selected=self.switch_page)
        self.tab_pages = AdwTStack(self.frame)

        self.tab_panel.column(expand="no")
        self.tab_pages.column()

    def switch_page(self):
        self.tab_pages.show_page(self.tab_panel.select())

    def add(self, page, text: str = ""):
        i = self.tab_panel.cget("items")
        i.append(text)
        self.tab_panel.configure(items=i)
        self.tab_pages.add_page(page, text)
        self.tab_pages.update()
        self.tab_panel.update()

    def destroy(self):
        self.tab_panel.destroy()
        self.tab_pages.destroy()
        super().destroy()


if __name__ == '__main__':
    root = Adwite(default_theme="win11")
    root.geometry("600x300")
    root.style_dark(True)


    def command():
        widgets_panel.show_page(choose_panel.select())


    def switch_theme(event):
        print(event)
        root.set_default_theme("bilibili", root.get_system_theme())


    root.bind("<<SystemThemeSwitch>>", switch_theme)

    choose_panel = AdwTListBox(
        items=sorted(
            ["AdwTButton", "AdwTCircularButton", "AdwTDesignerFrame", "AdwTEntry", "AdwTMDI", "AdwTTabs"]
        ),
        item_selected=command
    )
    choose_panel.column(expand=False, padx=(15, 5), pady=15, ipadx=5, ipady=5)

    widgets_panel = AdwTStack()
    widgets_panel.column(padx=(5, 15), pady=15, ipadx=5, ipady=5)

    button_panel = AdwTFrame(widgets_panel.frame)
    button = AdwTButton(button_panel.frame, text="AdwTButton")
    button.row(expand="no")
    widgets_panel.add_page(button_panel, "AdwTButton")

    cbutton_panel = AdwTFrame(widgets_panel.frame)
    cbutton = AdwTCircularButton(cbutton_panel.frame, text="AdwTCircularButton")
    cbutton.row(expand="no", fill="none")
    widgets_panel.add_page(cbutton_panel, "AdwTCircularButton")

    designerframe_panel = AdwTFrame(widgets_panel.frame)
    designerframe = AdwTDesignerFrame(designerframe_panel.frame, widget=AdwTButton, text="AdwTDesignerFrame")
    designerframe.place(x=5, y=5, width=160, height=60)
    widgets_panel.add_page(designerframe_panel, "AdwTDesignerFrame")

    entry_panel = AdwTFrame(widgets_panel.frame)
    entry = AdwTEntry(entry_panel.frame)
    entry.row(expand="no")
    widgets_panel.add_page(entry_panel, "AdwTEntry")

    mdi_panel = AdwTFrame(widgets_panel.frame)
    mdi = AdwTMDI(mdi_panel.frame)
    mdi_child1 = mdi.create_child()
    mdi.row()
    widgets_panel.add_page(mdi_panel, "AdwTMDI")

    tabs = AdwTTabs(widgets_panel.frame)
    for i in range(5):
        f = AdwTFrame(tabs.tab_pages.frame)
        l = AdwTLabel(f.frame, text=i)
        l.row()
        tabs.add(f, f"AdwTTab {i}")
    tabs.row()
    widgets_panel.add_page(tabs, "AdwTTabs")

    choose_panel.select("AdwTButton")
    widgets_panel.show_page("AdwTButton")

    root.mainloop()
