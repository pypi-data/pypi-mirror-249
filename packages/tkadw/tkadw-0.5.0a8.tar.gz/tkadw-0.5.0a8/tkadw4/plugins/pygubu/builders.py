from tkadw4.windows.theme import Adwite, AdwTFrame

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _


_designer_tab_label = _("TkAdwite")
_plugin_uid = "tkadw4"


class AdwiteBuilder(BuilderObject):
    class_ = Adwite
    container = True


class AdwTFrameBuilder(BuilderObject):
    class_ = AdwTFrame

    container = True


register_widget(
    f'{_plugin_uid}.AdwTFrame', AdwTFrameBuilder,
    'AdwTFrame',
    ('ttk', _designer_tab_label)
)

