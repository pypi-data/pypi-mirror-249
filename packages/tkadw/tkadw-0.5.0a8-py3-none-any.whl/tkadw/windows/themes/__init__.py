from .ant import AdwAntTheme
from .theme import AdwTheme, themepath
from .themebuilder import AdwSimpleThemeBuilder
from .win11 import AdwWin11Theme
from .win11 import AdwWin11Theme as AdwWindows11Theme
from .win11 import AdwWin11Theme as AdwSunValleyTheme
from .win11 import AdwWin11Theme as AdwFluentTheme


def nametotheme(name: str, *args, **kwargs):
    name = name.lower()
    if name == "win11" or name == "windows11" or name == "sunvalley" or name == "fluent":
        return AdwWin11Theme(*args, **kwargs)
    elif name == "ant":
        return AdwAntTheme(*args, **kwargs)