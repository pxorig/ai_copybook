# -*- coding: utf-8 -*-

import json
import traceback
import tornado.web
from src.ocr import ocr

# OCRHandler ocr 算法接口
class OCRHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body
        try:
            request = json.loads(data)
            url = request.get('url', None)
            if url is None:
                self.finish({
                    "status": -3,
                    "msg": "bad params: url is empty"
                })
                return
            result = ocr.recognition(url=url)
            self.finish({
                "status": 0,
                "msg": "ok",
                "data": result
            })
        except Exception as e:
            traceback.print_exc(e)
            self.finish({
                "status": -3,
                "msg": "ocr error"
            })