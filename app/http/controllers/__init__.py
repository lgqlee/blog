#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
from extended.session import SessionManager


class Controller(tornado.web.RequestHandler):
    def initialize(self):
        self.session_manager = SessionManager(self)

    @property
    def session(self):
        return self.session_manager.session

    def on_finish(self, chunk=None):
        self.session_manager.save()

    def set_default_headers(self):
        self._headers["Server"] = "nginx/1.1.19"