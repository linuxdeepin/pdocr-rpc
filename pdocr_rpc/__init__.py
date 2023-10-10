#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
import json
import os
from time import sleep
from xmlrpc.client import Binary
from xmlrpc.client import ServerProxy

from pdocr_rpc.conf import setting

os.environ["DISPLAY"] = ":0"

if setting.IS_LINUX:
    import pyscreenshot as ImageGrab
elif setting.IS_WINDOWS:
    from PIL import ImageGrab
    
from funnylog import logger


class OCR:
    @staticmethod
    def _pdocr_client(lang, picture_abspath=None, retry: int = 2):
        """
         通过 RPC 协议进行 OCR 识别。
        :return: 返回 PaddleOCR 的原始数据
        """
        if not picture_abspath:
            picture_abspath = setting.SCREEN_CACHE
            if setting.IS_X11:
                ImageGrab.grab().save(os.path.expanduser(picture_abspath))
            else:
                picture_abspath = (
                    os.popen("qdbus org.kde.KWin /Screenshot screenshotFullscreen")
                    .read()
                    .strip("\n")
                )
        server = ServerProxy(
            f"http://{setting.SERVER_IP}:{setting.PORT}", allow_none=True
        )
        put_handle = open(os.path.expanduser(picture_abspath), "rb")
        for _ in range(retry):
            try:
                # 将图片上传到服务端
                pic_dir = server.image_put(Binary(put_handle.read()))
                put_handle.close()
                # 返回识别结果
                return server.paddle_ocr(pic_dir, lang)
            except OSError:
                pass
            raise EnvironmentError(
                f"RPC服务器链接失败. http://{setting.SERVER_IP}:{setting.PORT}"
            )

    @classmethod
    def _ocr(
        cls,
        *target_strings,
        picture_abspath=None,
        similarity=0.6,
        return_default=False,
        return_first=False,
        lang="ch",
        retry: int = 2,
    ):
        """
         通过 OCR 进行识别。
        :param target_strings:
            目标字符,识别一个字符串或多个字符串,并返回其在图片中的坐标;
            如果不传参，返回图片中识别到的所有字符串。
        :param picture_abspath: 要识别的图片路径，如果不传默认截取全屏识别。
        :param similarity: 匹配度。
        :param return_default: 返回识别的原生数据。
        :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
        :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
        :param retry: 连接服务器重试次数
        :return: 返回的坐标是目标字符串所在行的中心坐标。
        """
        results = cls._pdocr_client(picture_abspath=picture_abspath, lang=lang, retry=retry)[0]
        if return_default:
            return results
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
                logger.debug(f"OCR识别到字符 [{target_strings[0]}]—>{center_x, center_y}")
                return center_x, center_y
            if len(more_map) > 1:
                logger.debug(f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}")
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
                logger.debug(f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}")
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
                logger.debug(f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}")
                return more_map
        res_log = []
        for res in results:
            [[*_], [strings, rate]] = res
            res_log.append(strings)
        logger.debug(f"未识别到字符{target_strings}, 识别到的原始内容：{res_log}")
        return False

    @classmethod
    def ocr(
            cls,
            *target_strings,
            picture_abspath=None,
            similarity=0.6,
            return_default=False,
            return_first=False,
            lang="ch",
            retry: int = 2,
            res_retry: int = 2,
    ):
        """
        通过 OCR 进行识别。
        :param target_strings:
            目标字符,识别一个字符串或多个字符串,并返回其在图片中的坐标;
            如果不传参，返回图片中识别到的所有字符串。
        :param picture_abspath: 要识别的图片路径，如果不传默认截取全屏识别。
        :param similarity: 匹配度。
        :param return_default: 返回识别的原生数据。
        :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
        :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
        :param retry: 连接服务器重试次数
        :param res_retry: 如果结果返回为 False，重试次数
        :return: 返回的坐标是目标字符串所在行的中心坐标。
        """
        for _ in range(res_retry):
            res = cls._ocr(
                *target_strings,
                picture_abspath=picture_abspath,
                similarity=similarity,
                return_default=return_default,
                return_first=return_first,
                lang=lang,
                retry=retry,
            )
            if res is False:
                sleep(1)
                continue
            return res
        return False


if __name__ == "__main__":
    from pdocr_rpc.conf import setting
    setting.SERVER_IP = "youqu-dev.uniontech.com"
    OCR.ocr("uniontech","youqu")
