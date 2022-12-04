#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Author: Mikigo
@Date: 2022/5/25 0:03
"""
import json
from os import popen, environ
from xmlrpc.client import Binary
from xmlrpc.client import ServerProxy
from config import IS_X11
from config import IP
# IP = "10.8.13.78"
from config import PORT
environ["DISPLAY"] = ":0"
import pyscreenshot



def _pdocr(lang):
    """
     通过 RPC 协议进行 OCR 识别。
    :return: OCR 识别结果
    """
    # 截取当前屏幕
    from config import SCREEN_CACHE
    if IS_X11:
        pyscreenshot.grab().save(SCREEN_CACHE)
    else:
        SCREEN_CACHE = (
            popen("qdbus org.kde.KWin /Screenshot screenshotFullscreen")
            .read()
            .strip("\n")
        )
    server = ServerProxy(f"http://{IP}:{PORT}", allow_none=True)
    put_handle = open(SCREEN_CACHE, "rb")
    try:
        server.image_put(Binary(put_handle.read()))
        put_handle.close()
        return server.paddle_ocr("screen.png", lang)
    except OSError:
        raise EnvironmentError(f"RPC服务器链接失败. http://{IP}:{PORT}")


def ocr(*target_strings, similarity=0.6, return_first=False, lang="ch"):
    """
     从 OCR 识别结果中判断是否存在目标字符。
    :param target_strings: 目标字符,识别一个字符串或多个字符串;如果不传参，返回当前屏幕中识别到的所有字符串。
    :param similarity: 匹配度。
    :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
    :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
    :return: 返回的坐标是目标字符串所在行的中心坐标。
    """
    results = _pdocr(lang=lang)
    more_map = {}
    if len(target_strings) == 1:
        n = 1
        for res in results:
            [
                [
                    [left_top_x, left_top_y],
                    [right_top_x, right_top_y],
                    [right_bottom_x, right_bottom_y],
                    [left_bottom_x, left_bottom_y],
                ],
                (strings, rate),
            ] = res
            if target_strings[0] in strings:
                if rate >= similarity:
                    center_x = (right_top_x + left_top_x) / 2
                    center_y = (right_bottom_y + right_top_y) / 2
                    more_map[
                        target_strings[0]
                        if not more_map.get(target_strings[0])
                        else f"{target_strings[0]}_{n}"
                    ] = (center_x, center_y)
                    if return_first:
                        break
                    n += 1
        if len(more_map) == 1:
            center_x, center_y = more_map.get(target_strings[0])
            print(f"OCR识别到字符“{target_strings[0]}”—>{center_x, center_y}")
            return center_x, center_y
        if len(more_map) > 1:
            print(
                f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}"
            )
            return more_map

    elif len(target_strings) == 0:
        for res in results:
            [
                [
                    [left_top_x, left_top_y],
                    [right_top_x, right_top_y],
                    [right_bottom_x, right_bottom_y],
                    [left_bottom_x, left_bottom_y],
                ],
                (strings, rate),
            ] = res
            if rate >= similarity:
                center_x = (right_top_x + left_top_x) / 2
                center_y = (right_bottom_y + right_top_y) / 2
                more_map[strings] = (center_x, center_y)

        if more_map:
            print(
                f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}"
            )
            return more_map

    else:
        for target_string in target_strings:
            n = 1
            more_map[target_string] = False
            for res in results:
                [
                    [
                        [left_top_x, left_top_y],
                        [right_top_x, right_top_y],
                        [right_bottom_x, right_bottom_y],
                        [left_bottom_x, left_bottom_y],
                    ],
                    (strings, rate),
                ] = res
                if target_string in strings and rate >= similarity:
                    center_x = (right_top_x + left_top_x) / 2
                    center_y = (left_bottom_y + left_top_y) / 2
                    if more_map.get(target_string):
                        _key = f"{target_string}_{n}"
                    else:
                        _key = target_string
                        n = 1
                    more_map[_key] = (center_x, center_y)
                    if return_first:
                        break
                    n += 1

        if more_map:
            print(
                f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}"
            )
            return more_map

    print(f"未识别到字符{f'“{target_strings}”' or ''}")
    return False

if __name__ == '__main__':
    ocr()