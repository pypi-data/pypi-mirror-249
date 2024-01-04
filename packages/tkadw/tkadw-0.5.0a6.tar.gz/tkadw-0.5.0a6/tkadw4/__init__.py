from tkadw4.windows.widgets import *
from tkadw4.utility.appconfig import appconfig as AdwReadAppConfig

from tkadw4.windows import *

# 0.3.0加入
from tkadw4.windows.theme import *

from tkadw4.game import *

# 0.3.5加入
from tkadw4.layout import *

# 0.3.9加入
from tkadw4.designer.designerframe import AdwDesignerFrame
from tkadw4.designer.designer import AdwDesigner
from tkadw4.designer.builder import AdwBuilder

try:
    from tkadw_material import *
except ModuleNotFoundError:
    pass

# from tkadw4.tkite import * 已废弃移除
# from tkadw4.win11 import * 已废弃移除
# from tkadw4.advanced import * 已废弃移除，改为from tkadw4.adw import Adw导入
# from tkadw4.bilibili import BiliBiliButton, BiliBiliDarkButton, BiliBiliFrame, BiliBiliDarkFrame, \
#     BiliBiliEntry, BiliBiliDarkEntry, BiliBiliDarkTextBox, BiliBiliTextBox 已废弃移除

# 0.3.7补充
from tkadw4.utility import *


def get_version():
    return "0.4.9"


def get_major_version():
    return "0"


def get_micro_version():
    return "4"


if __name__ == '__main__':
    from tkinter import Tk, Toplevel

    root = Tk()

    adw_run(root)
