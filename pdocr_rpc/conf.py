#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
import enum
import os
import sys


@enum.unique
class DisplayServer(enum.Enum):
    wayland = "wayland"
    x11 = "x11"


@enum.unique
class PlatForm(enum.Enum):
    win = "win32"
    linux = "linux"


class _Setting:
    """配置模块"""

    SERVER_IP = "127.0.0.1"
    PORT = 8891

    IS_LINUX = False
    IS_WINDOWS = False
    if sys.platform == PlatForm.win.value:
        # windows
        IS_WINDOWS = True
        # TODO
        ...
    elif sys.platform == PlatForm.linux.value:
        # Linux
        IS_LINUX = True
        # 显示服务器
        DISPLAY_SERVER = (
            os.popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
            .read()
            .split("=")[-1]
            .strip("\n")
        )

        IS_X11 = DISPLAY_SERVER == DisplayServer.x11.value
        IS_WAYLAND = DISPLAY_SERVER == DisplayServer.wayland.value
        SCREEN_CACHE = "/tmp/screen.png"


setting = _Setting()
