from pdocr_rpc import OCR
from pdocr_rpc.conf import setting

setting.SERVER_IP = "10.8.13.78"
setting.PORT = 8888
OCR.ocr("OCR")