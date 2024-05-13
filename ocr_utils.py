#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=E0401,C0413,R0903,W0707,W0611
import random
import time

try:
    import cv2 as cv

    GET_OPENCV_FORM_RPC = False
except ModuleNotFoundError:
    GET_OPENCV_FORM_RPC = True

from pdocr_rpc import OCR as _OCR
from pdocr_rpc.conf import setting as ocr_setting

import youqu_conf as conf


class OCRUtils:
    ocr_setting.NETWORK_RETRY = int(conf.OCR_NETWORK_RETRY)
    ocr_setting.PAUSE = float(conf.OCR_PAUSE)
    ocr_setting.TIMEOUT = float(conf.OCR_TIMEOUT)
    ocr_setting.MAX_MATCH_NUMBER = int(conf.OCR_MAX_MATCH_NUMBER)
    ocr_setting.PORT = conf.OCR_PORT
    ocr_servers = [i.strip() for i in conf.OCR_SERVER_HOST.split("/") if i]
    x = None
    y = None

    @classmethod
    def ocr(cls, *args, **kwargs):
        """ocr load balance"""
        servers = cls.ocr_servers
        while servers:
            ocr_setting.SERVER_IP = random.choice(servers)
            check_start = time.time()
            if _OCR.check_connected() is False:
                servers.remove(ocr_setting.SERVER_IP)
                ocr_setting.SERVER_IP = None
            else:
                check_end = time.time()
                print("check_connected：", check_end - check_start, "s")
                break
        if ocr_setting.SERVER_IP is None:
            raise EnvironmentError(f"所有OCR服务器不可用: {cls.ocr_servers}")
        ocr_start = time.time()
        result = _OCR.ocr(*args, **kwargs)
        ocr_end = time.time()
        print("ocr session：",ocr_end - ocr_start, "s")
        return result


if __name__ == '__main__':
    for i in range(1):
        start = time.time()
        OCRUtils.ocr("所有")
        end = time.time()
        print("总耗时：",end - start, "s")
