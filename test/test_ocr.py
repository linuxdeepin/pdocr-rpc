#!/usr/bin/python3
import pytest

from pdocr_rpc.ocr import OCR

from pdocr_rpc.setting import setting

setting.SERVER_IP = "10.8.13.78"
setting.PORT = "8890"

def test_ocr():
    res = OCR.ocr()
    assert res is not None

if __name__ == '__main__':
    pytest.main()