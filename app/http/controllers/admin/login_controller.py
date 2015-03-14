#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.gen

from app.http.controllers import Controller
from extended.quotes import generate


class AdminLoginController(Controller):
    def get(self):
        if not self.get_current_user():
            return self.render('admin/login.html', quote=generate())
        self.redirect("/admin")

    @tornado.gen.coroutine
    def post(self):
        (email, password) = (self.get_argument("email", None), self.get_argument("password", None))
        if not email or not password:
            return self.send_error(400)
        user = yield self._auth_password(email, password)
        if not user:
            # todo 需要在 redis 中做限制，连续三次失败该 IP 禁用一个小时
            return self.write({"code": 403, "message": "Email and password not match"})
        token = yield self.update_token(user)
        if token:
            for item in self.SESSION_USER_INFO:
                self.session[item] = str(user[item])
            if self.get_argument('remember', False):
                self._generate_auth_cookie(token)
            return self.write({"code": 200})
        self.write({"code": 500, "message": "Login with error, please try again"})