#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 15:05:06
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com


import uuid
import hashlib


class Session(object):

    def __init__(self, session_data=None):
        self.__data = session_data or {}

    def __setitem__(self, key, value):
        """
        操作 session 内容，如果 value 为 None 则视为删除
        """
        if self.__data.get(key, None) is value:
            return
        if value is None:
            del self.__data[key]
            return
        self.__data[key] = value

    def __getitem__(self, item):
        return self.__data.get(item, None)

    def destroy(self):
        """
        清空当前 session 内容
        """
        self.__data.clear()

    def update(self, kwags):
        """
        批量更新 session
        """
        self.__data.update(kwags)

    def __delitem__(self, key):
        del self.__data[key]

    def dump(self):
        return {item: self.__data[item] for item in self.__data if self.__data[item]}


class SessionManger(object):
    DEFAULT_SESSION_NAME = "B_SESSION"

    def __init__(self, handler, store, **kwargs):
        self.__store = store
        self.__handler = handler
        self.__session_name = kwargs.get(
            'session_name', self.DEFAULT_SESSION_NAME)
        self.__session = None
        self.session_id = self.__handler.get_secure_cookie(self.__session_name)
        self.initialize()

    def initialize(self):
        """
        初始化
        如果不存在对应的 cookie 则生成新的 session_id，并设置 cookie
        存在的话则从 redis 取出内容并返回 Session 对象
        """
        is_new = False
        if not self.session_id:
            is_new = True
            self.session_id = str(self._generate_id())
            self.__handler.set_secure_cookie(
                self.__session_name, self.session_id, httponly=True)
        else:
            self.session_id = self.session_id.decode("utf-8", "strict")
        self.__session = Session(
            not is_new and self.__store.get(self.session_id)
        )

    @property
    def session(self):
        return self.__session

    def save(self):
        """
        将 redis 的内存写入到 sessioinStore 中
        """
        self.__store.set(self.session_id, self.session.dump())

    @staticmethod
    def _generate_id():
        new_id = hashlib.sha256(str(uuid.uuid4()).encode("utf8"))
        return str(new_id.hexdigest())
