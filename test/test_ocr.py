#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
import pytest

from pdocr_rpc import OCR

from pdocr_rpc.conf import setting

setting.SERVER_IP = "10.8.13.78"
setting.PORT = "8890"

def test_ocr():
    res = OCR.ocr()
    assert res is not None

if __name__ == '__main__':
    pytest.main()