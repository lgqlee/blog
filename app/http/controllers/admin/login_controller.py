#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.gen
import json
import uuid
import hashlib
from passlib.hash import sha256_crypt

from app.http.controllers import Controller
from extended.quotes import generate
from extended.database import get_mongodb_connection


class AdminLoginController(Controller):
    __USER_AUTH_COOKIE = "PHP_SESSION"

    @tornado.gen.coroutine
    def get(self):
        # todo 判断 session，如果有登录则跳转/返回 json
        self.render('admin/login.html', quote=generate())

    @tornado.gen.coroutine
    def post(self):
        (email, password) = (self.get_argument("email", None), self.get_argument("password", None))
        if not email or not password:
            return self.send_error(400)
        coll = get_mongodb_connection().users
        user = yield coll.find_one({"email": email})
        if not user or not sha256_crypt.verify(password, user["password"]):
            return self.write({"code": 403, "message": "Email and password not match"})
        set_login = yield self.update_token(coll, user)
        if set_login:
            return self.write({"code": 200})
        self.write({"code": 500, "message": "Login with error, please try again"})

    @tornado.gen.coroutine
    def update_token(self, coll, user):
        token = hashlib.sha256(str(uuid.uuid4()).encode("utf8")).hexdigest()
        result = yield coll.update({"_id": user["_id"]}, {"$set": {"token": token}})
        if result['n'] < 1:
            return False
        for item in ("name", "_id", "role"):
            self.session[item] = str(user[item])
        if self.get_argument('remember', False):
            self._generate_auth_cookie(token)
        return True

    def _generate_auth_cookie(self, token):
        m = hashlib.md5()
        m.update(("{0}{1}".format(token, self.request.headers["User-Agent"])).encode("utf8"))
        self.set_secure_cookie(self.__USER_AUTH_COOKIE, m.hexdigest(), expires_days=365, httponly=True)