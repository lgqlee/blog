#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 15:36:31
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import tornado.gen
import tornado.web

from providers import session, db
from models import user as User


class Controller(tornado.web.RequestHandler):

    USER_AUTH_COOKIE = "PHP_SESSION"

    def initialize(self):
        self.session_manager = session.register(
            self, "redis", client=self.redis_client)

    @property
    def redis_client(self):
        """
        使用 connection_pool 的时候， redis 将在执行一次操作后回收该连接
        所以每次都要生成新的 connection
        """
        return db.get("redis")

    @property
    def mongo_client(self):
        return db.get("mongo")

    @property
    def session(self):
        return self.session_manager.session

    @property
    def is_ajax(self):
        """
        通过 header 信息当前请求是否是 ajax 请求
        """
        return self.request.headers.get("X-Requested-With", None) == "XMLHttpRequest"

    @tornado.gen.coroutine
    def prepare(self):
        """
        session 过期检查 cookie 中是否有登录信息
        对用户的 UA 以及 token 进行合并加密对比
        通过则恢复 session
        """
        print(self.is_ajax)
        if not self.session["_id"]:
            auth_cookie = self.get_secure_cookie(self.USER_AUTH_COOKIE, None)
            if not auth_cookie:
                return None
            user_id, md5_str = auth_cookie.decode("utf-8", "strict").split("|")
            if not md5_str:
                return None
            user = yield User.check_token(
                user_id, self.request.headers.get("User-Agent", None), md5_str)
            if not user:
                self.clear_cookie(self.USER_AUTH_COOKIE)
                return None
            self.session.update(user)

    def on_finish(self, chunk=None):
        return self.session_manager.save()

    def set_default_headers(self):
        self._headers["Server"] = "nginx/1.1.19"

    def get_current_user(self):
        if not self.session["_id"]:
            return None
        # 返回 session 中内容的副本，防止因为引用修改导致错误
        return self.session.dump().copy()

    def logout(self):
        self.session.destroy()
        self.clear_cookie(self.USER_AUTH_COOKIE)
