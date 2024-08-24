# -*- coding: utf-8 -*-

import tornado.web

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish({
            "status": 0,
            "msg": "health"
        })