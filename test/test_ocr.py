#!/usr/bin/python3
import pytest

from pdocr_rpc.ocr import ocr

def test_ocr():
    res = ocr()
    assert res is not None

if __name__ == '__main__':
    pytest.main()