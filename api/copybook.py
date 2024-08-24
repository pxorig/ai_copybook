# -*- coding: utf-8 -*-

import json
import traceback
import tornado.web

from src.copybook import font_type, copybook

font_path  = "./ttf"

# GetFontTypesHandler 获取字体类型列表
class GetFontTypesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            ttfs = font_type.get_list(path=font_path)
            self.finish({
                "status": 0,
                "msg": "ok", 
                "data": ttfs
            })
        except Exception as e:
            traceback.print_exc(e)
            self.finish({
                "status": -1,
                "msg": "get font types error"
            })

# GenCopybookHandler 生成字帖
class GenCopybookHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body
        try:
            requests = json.loads(data)
            words = requests.get("words", "")
            if len(words) == 0:
                self.finish({
                    "status": -3,
                    "msg": "bad params: words is empty"
                })
                return
            font = requests.get("font", "")
            ttfs = font_type.get_list(path=font_path)
            if font not in ttfs:
                self.finish({
                    "status": -3,
                    "msg": "bad params: font not in ttf list"
                })
                return
            # 生成字帖
            c = copybook.Copybook(words=words, font_size=200,font_path=f'{font_path}/{font}.ttf')
            img = c.gen()
            self.finish({
                "status": 0,
                "msg": "ok",
                "data": img
            })
        except Exception as e:
            traceback.print_exc(e)
            self.finish({
                "status": -2,
                "msg": "gen copybook error"
            })