#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web


class Controller(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def on_finish(self, chunk=None):
        pass