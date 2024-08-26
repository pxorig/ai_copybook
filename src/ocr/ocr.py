# -*- coding: utf-8 -*-

import cv2
import requests
import numpy as np

# import pycorrector
import os
import sys
sys.path.append(f'{os.getcwd()}/src/ocr/ppocronnx')
# print(sys.path)
from .ppocronnx.predict_system import TextSystem

text_sys = TextSystem()

def read_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is not None:
            return img
        else:
            print("Failed to decode image.")
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
    return None

# 检测并识别文本
def recognition(url: str) -> str:
    result = []
    img = read_image_from_url(url)
    res = text_sys.detect_and_ocr(img)
    # m = ProperCorrector()
    for boxed_result in res:
        result.append(boxed_result.ocr_text)
        # print("{}, {:.3f}".format(boxed_result.ocr_text, boxed_result.score))
    

    result = "\n".join(result)
    print(result)
    return result

# url = "https://sfsm.jmxy.cc/wimg/028d2c63c400080019043066dee.jpg"
# res = recognition(url=url)
# print(res)