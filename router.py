# -*- coding: utf-8 -*-

import tornado.web
import api

# 创建一个应用实例，并设置请求的路径对应的请求处理类
app = tornado.web.Application([
    (r"/", api.HealthHandler),
    (r"/font/", api.GetFontTypesHandler),
    (r"/gen/", api.GenCopybookHandler),
    (r"/ocr/", api.OCRHandler),
])