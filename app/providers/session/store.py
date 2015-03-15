#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 14:27:13
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com


import ujson


class Store(object):

    STRING_TYPE = type("")

    def set(self, session_id, content):
        raise NotImplementedError

    def get(self, seesion_id):
        raise NotImplementedError

    def dumps(self, content):
        """
        对内容进行处理，如果是非字符串，则进行 json 格式转化
        """
        return content if type(content) is self.STRING_TYPE else ujson.dumps(content)

    @staticmethod
    def loads(content):
        return ujson.loads(content)


class RedisStore(Store):

    # session 默认过期时间
    DEFAULT_EXPIRE = 60 * 60 * 12
    # session 在 redis 中默认的前缀
    DEFAULT_PREFIX = "session"

    def __init__(self, client, **kwargs):
        self.__expire = kwargs.get("expire", self.DEFAULT_EXPIRE)
        self.__prefix = kwargs.get("prefix", self.DEFAULT_PREFIX)
        self.__client = client

    def __session_key(self, session_id):
        return "{prefix}:{session_id}".format(
            prefix=self.__prefix, session_id=session_id)

    def set(self, session_id, content):
        """
        将 session 的内容变成字符串后写入 redis
        """
        session_key = self.__session_key(session_id)
        if not content or len(content) is 0:
            return self.__client.delete(session_key)
        self.__client.setex(session_key, self.dumps(content), self.__expire)

    def get(self, session_id):
        session_key = self.__session_key(session_id)
        content = self.__client.get(session_key)
        return content and self.loads(content)
