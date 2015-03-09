#!/usr/bin/python
# -*- coding: utf-8 -*-

import ujson

from extended.session import SessionManager, SESSION_PREFIX, DAY, SESSION_EXPIRE
from extended.database import get_redis_connection


redis_conn = get_redis_connection()


class FakeHandler(object):
    def __init__(self):
        self._cookie_container = {}

    def set_secure_cookie(self, name, value, **kwargs):
        print(kwargs)
        self._cookie_container[name] = value

    def get_secure_cookie(self, name):
        return self._cookie_container.get(name, None)


sm = SessionManager(FakeHandler())


def test_init():
    assert sm.session_id is not None


def test_set():
    sm.session["name"] = "vincent"
    sm.save()
    assert redis_conn.get(SESSION_PREFIX + sm.session_id) == '{"name":"vincent"}'
    sm.session["name"] = None
    sm.save()
    assert redis_conn.get(SESSION_PREFIX + sm.session_id) is None
    sm.session["name"] = "alvin"
    sm.save()
    assert redis_conn.get(SESSION_PREFIX + sm.session_id) == '{"name":"alvin"}'
    del sm.session["name"]
    sm.save()
    assert redis_conn.get(SESSION_PREFIX + sm.session_id) is None


def test_del():
    sm.session["name"] = "vincent"
    sm.session["age"] = 16
    sm.save()
    data = ujson.loads(redis_conn.get(SESSION_PREFIX + sm.session_id))
    assert data["age"] is 16
    sm.session.destroy()
    sm.save()
    assert redis_conn.get(SESSION_PREFIX + sm.session_id) is None


def test_expire():
    sm.session["name"] = "vincent"
    sm.save()
    exp1 = redis_conn.ttl(SESSION_PREFIX + sm.session_id)
    assert DAY * SESSION_EXPIRE - exp1 < 10
    sm.session.destroy()
    sm.save()