#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.gen
import tornado.web

from extended.database import get_mongodb_connection
from extended.session import SessionManager
from app.http.mixins.user_mixin import UserMixin


class Controller(tornado.web.RequestHandler, UserMixin):
    def initialize(self):
        self.session_manager = SessionManager(self)
        self.conn = get_mongodb_connection()

    @tornado.gen.coroutine
    def prepare(self):
        if not self.session["_id"]:
            user = yield self._check_auth_cookie()
            if not user:
                self.clear_cookie(self.USER_AUTH_COOKIE)
                return None
            for item in self.SESSION_USER_INFO:
                self.session[item] = str(user[item])

    @property
    def session(self):
        return self.session_manager.session

    def on_finish(self, chunk=None):
        self.session_manager.save()

    def set_default_headers(self):
        self._headers["Server"] = "nginx/1.1.19"

    def get_current_user(self):
        if not self.session["_id"]:
            return None
        return {item: self.session[item] for item in self.SESSION_USER_INFO}

    def logout(self):
        self.session.destroy()
        self.clear_cookie(self.USER_AUTH_COOKIE)