#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import uuid
import ujson

from extended.database import get_redis_connection

SESSION_NAME = "B_SESSION"
SESSION_EXPIRE = 1
SESSION_PREFIX = "blog:session:"
DAY = 60 * 60 * 24
"""
请求中的 session 方法
支持操作如下：
1. 赋值
    self.session["key"] = value
2. 取值
    print(self.session["key"])
3. 删除某值
    del self.session["key"]
    sel.session["key"] = None
4. 删除所有的值
    self.session.destroy()
"""


class Session(object):
    def __init__(self, session_data=None):
        self._data = session_data and ujson.loads(session_data) or {}

    def __setitem__(self, key, value):
        if self._data.get(key, None) is value:
            return
        if value is None:
            del self._data[key]
            return
        self._data[key] = value

    def __getitem__(self, item):
        return self._data.get(item, None)

    def destroy(self):
        self._data = {}

    def __delitem__(self, key):
        del self._data[key]

    def dump(self):
        if len(self._data) is 0:
            return None
        return ujson.dumps(self._data)


class SessionManager(object):
    def __init__(self, handler):
        self._redis_conn = get_redis_connection()
        self._handler = handler
        self._session = None
        self.session_id = self._handler.get_secure_cookie(SESSION_NAME)
        self.initialize()

    def initialize(self):
        if not self.session_id:
            self.session_id = str(self._generate_id())
            self._handler.set_secure_cookie(SESSION_NAME, self.session_id, httponly=True)
        else:
            self.session_id = self.session_id.decode("utf-8", "strict")
        self._session = Session(
            self._redis_conn.get(SESSION_PREFIX + self.session_id)
        )

    @property
    def session(self):
        return self._session

    def save(self):
        data = self.session.dump()
        session_key = SESSION_PREFIX + self.session_id
        if not data:
            self._redis_conn.delete(session_key)
            return
        self._redis_conn.setex(session_key, data, DAY * SESSION_EXPIRE)

    @staticmethod
    def _generate_id():
        new_id = hashlib.sha256(str(uuid.uuid4()).encode("utf8"))
        return new_id.hexdigest()