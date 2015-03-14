#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.gen
import tornado.web
import hashlib
from bson.objectid import ObjectId

from extended.session import SessionManager
from extended.database import get_mongodb_connection


class Controller(tornado.web.RequestHandler):
    USER_AUTH_COOKIE = "PHP_SESSION"
    SESSION_USER_INFO = ("name", "_id", "role", "email")

    def initialize(self):
        self.session_manager = SessionManager(self)

    @tornado.gen.coroutine
    def prepare(self):
        if not self.session["_id"]:
            user = yield self._check_auth_cookie()
            if not user:
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
        user = {}
        for item in self.SESSION_USER_INFO:
            user[item] = self.session[item]
        return user

    @tornado.gen.coroutine
    def _check_auth_cookie(self):
        auth_cookie = self.get_secure_cookie(self.USER_AUTH_COOKIE, None)
        if not auth_cookie:
            return False
        (user_id, md5_str) = auth_cookie.decode("utf-8", "strict").split("|")
        if not md5_str:
            self.clear_cookie(self.USER_AUTH_COOKIE)
            return False
        coll = get_mongodb_connection().users
        user = yield coll.find_one({"_id": ObjectId(user_id)})
        if not user:
            self.clear_cookie(self.USER_AUTH_COOKIE)
            return False
        m = hashlib.md5()
        m.update(("{0}{1}".format(user["token"], self.request.headers["User-Agent"])).encode("utf8"))
        return m.hexdigest() == md5_str and user

    def _generate_auth_cookie(self, token):
        m = hashlib.md5()
        m.update(("{0}{1}".format(token, self.request.headers["User-Agent"])).encode("utf8"))
        self.set_secure_cookie(self.USER_AUTH_COOKIE, "{0}|{1}".format(self.session["_id"], m.hexdigest()),
                               expires_days=365, httponly=True)

    def logout(self):
        self.session.destroy()
        self.clear_cookie(self.USER_AUTH_COOKIE)