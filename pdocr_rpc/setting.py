import enum
import os
import platform
import sys


@enum.unique
class DisplayServer(enum.Enum):
    wayland = "wayland"
    x11 = "x11"

@enum.unique
class PlatForm(enum.Enum):
    win = "win"
    linux = "linux"



class _Setting:
    """配置模块"""

    IP = "0.0.0.0"
    PORT = 8890

    if sys.platform == "win32":
        # windows
        IS_WINDOWS = True
        # TODO
        ...
    elif platform.system() == PlatForm.linux:
        # Linux
        IS_LINUX = True
        # 显示服务器
        DISPLAY_SERVER = os.popen(
            "cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1"
        ).read().split("=")[-1].strip("\n")

        IS_X11 = (DISPLAY_SERVER == DisplayServer.x11)
        IS_WAYLAND = (DISPLAY_SERVER == DisplayServer.wayland)
        SCREEN_CACHE = "/tmp/screen.png"


setting = _Setting()
