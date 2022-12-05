from os import popen


class DisplayServer:
    wayland = "wayland"
    x11 = "x11"


# 显示服务器
DISPLAY_SERVER = popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1").read() \
    .split("=")[-1].strip("\n")

IS_X11 = (DISPLAY_SERVER == DisplayServer.x11)
IS_WAYLAND = (DISPLAY_SERVER == DisplayServer.wayland)
IP = popen("hostname -I").read().split(" ")[0]
PORT = 8890
SCREEN_CACHE = "/tmp/screen.png"
