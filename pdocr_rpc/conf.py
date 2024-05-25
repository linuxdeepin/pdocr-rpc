#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
import enum
import os
import platform
import tempfile


@enum.unique
class DisplayServer(enum.Enum):
    wayland = "wayland"
    x11 = "x11"


@enum.unique
class PlatForm(enum.Enum):
    # win = "win32"
    # linux = "linux"
    win = "Windows"
    linux = "Linux"
    macos = "Darwin"


class _Setting:
    """配置模块"""

    SERVER_IP = "127.0.0.1"
    PORT = 8890
    NETWORK_RETRY = 1
    PAUSE = 1
    TIMEOUT = 5
    MAX_MATCH_NUMBER = 100

    IS_LINUX = False
    IS_WINDOWS = False
    IS_MACOS = False

    SCREEN_CACHE = os.path.join(tempfile.gettempdir(), 'screen.png')  # SCREEN_CACHE = "/tmp/screen.png"

    if platform.system() == PlatForm.win.value:
        # windows
        IS_WINDOWS = True
        IS_X11 = False
        IS_WAYLAND = False
        print("IS_X11======", IS_X11)
        print("IS_WAYLAND======", IS_WAYLAND)
    elif platform.system() == PlatForm.macos.value:
        # MacOS
        IS_MACOS = True
        IS_X11 = False
        IS_WAYLAND = False
        print("IS_X11======", IS_X11)
        print("IS_WAYLAND======", IS_WAYLAND)
    elif platform.system() == PlatForm.linux.value:
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
        print("IS_X11======",IS_X11)
        print("IS_WAYLAND======", IS_WAYLAND)


setting = _Setting()
