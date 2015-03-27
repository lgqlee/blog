#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 19:57:49
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import tornado.gen

from providers import qoutes
from controllers import Controller, Route
from models import user as User


@Route("/admin/login")
class AdminLoginController(Controller):

    def get(self):
        if not self.current_user:
            return self.render('admin/login.html', quote=qoutes.rand())
        self.redirect("/admin")

    @tornado.gen.coroutine
    def post(self):
        if self.current_user:
            return self.write({"code": 200})
        email, password = (
            self.get_argument("email", None),
            self.get_argument("password", None)
        )
        # 参数不完整直接返回 http 错误
        if not email or not password:
            return self.send_error(400)
        user = yield User.auth_by_password(email, password)
        if not user:
            # todo 需要在 redis 中做限制，三十分钟内连续三次失败该 IP 禁用一个小时
            return self.write({
                "code": 412,
                "message": "Email and password not match"
            })
        token = yield User.update_token(user["_id"])
        if token:
            self.session.update(user)
            if self.get_argument('remember', False):
                voucher = User.encrypt_by_token(
                    token,
                    self.request.headers["User-Agent"]
                )
                self.set_secure_cookie(
                    self.USER_AUTH_COOKIE, voucher, expires_days=120, version=None)
                return self.write({"code": 200})
        # 生成 token 失败返回 500
        self.write({
            "code": 500,
            "message": "Login with error, please try again"
        })
