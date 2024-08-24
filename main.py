# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web

import router

# 启动 HTTP 服务器
if __name__ == "__main__":
    router.app.listen(80)
    tornado.ioloop.IOLoop.current().start()