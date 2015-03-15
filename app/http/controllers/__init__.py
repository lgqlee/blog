#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 15:36:31
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import redis
import motor
import tornado.gen
import tornado.web

from providers import session
from config import database
from user_mixin import UserMixin

mongo_config = database["mongo"]
connection_pools = {
    "redis": redis.ConnectionPool(**database["redis"]),
    "mongo": motor.MotorClient(mongo_config["host"])[mongo_config["database"]]
}


class Controller(tornado.web.RequestHandler, UserMixin):

    __db_clients = {}

    def initialize(self):
        self.session_manager = session.register(
            self, "redis", client=self.redis_client)

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
    def redis_client(self):
        c = self.__db_clients.get("redis", None)
        if c:
            return c
        self.__db_clients["redis"] = redis.Redis(
            connection_pool=connection_pools["redis"])
        return self.redis_client

    @property
    def mongo_client(self):
        c = self.__db_clients.get("mongo", None)
        if c:
            return c
        self.__db_clients["mongo"] = connection_pools["mongo"]
        return self.mongo_client

    @property
    def session(self):
        return self.session_manager.session

    @property
    def is_ajax(self):
        return self.get_argument("ajax", False)

    def on_finish(self, chunk=None):
        return self.session_manager.save()

    def set_default_headers(self):
        self._headers["Server"] = "nginx/1.1.19"

    def get_current_user(self):
        if not self.session["_id"]:
            return None
        return {item: self.session[item] for item in self.SESSION_USER_INFO}

    def logout(self):
        self.session.destroy()
        self.clear_cookie(self.USER_AUTH_COOKIE)
