#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
from pdocr_rpc import OCR
from pdocr_rpc.conf import setting

setting.SERVER_IP = "10.8.13.78"
# setting.PORT = 8890
OCR.ocr(picture_abspath="~/Desktop/1.png")