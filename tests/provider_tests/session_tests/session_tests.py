#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-16 17:05:20
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _

from app.providers import session
from app.providers.session.store import RedisStore
from app.providers import db

redis_client = db.get("redis")
redis_store = RedisStore(redis_client)


class FakeHandler(object):

    def __init__(self, cookie_container=None):
        self._cookie_container = cookie_container or {}
        self.session_manager = session.register(
            self, "redis", client=redis_client)

    def set_secure_cookie(self, name, value, **kwargs):
        print(kwargs)
        self._cookie_container[name] = value

    @property
    def session(self):
        return self.session_manager.session

    def get_secure_cookie(self, name):
        cookie = self._cookie_container.get(name, None)
        return cookie and cookie.encode('utf-8')

handler = FakeHandler()


def test_generate_session():
    handler.session["name"] = "vincent"
    handler.session_manager.save()
    s = redis_store.get(handler.session_manager.session_id)
    assert s["name"] == "vincent"


def test_session_set_none():
    handler.session["name"] = "vincent"
    handler.session["name"] = None
    handler.session_manager.save()
    assert redis_store.get(handler.session_manager.session_id) is None


def test_session_get():
    assert handler.session["name"] == None


def test_session_destroy():
    handler.session["age"] = 16
    handler.session["name"] = "alvin"
    assert len(handler.session.dump()) == 2
    handler.session.destroy()
    handler.session_manager.save()
    assert redis_store.get(handler.session_manager.session_id) is None


def test_multi_update():
    handler.session.update({"name": "vt", "age": 21})
    handler.session_manager.save()
    assert len(redis_store.get(handler.session_manager.session_id)) == 2


def test_session_from_cookie():
    handler.session.update({"name": "vt", "age": 23})
    handler.session_manager.save()
    new_handler = FakeHandler({
        handler.session_manager.DEFAULT_SESSION_NAME: handler.session_manager.session_id
    })
    s = redis_store.get(new_handler.session_manager.session_id)
    assert s["age"] == 23
    del new_handler.session["age"]
    new_handler.session_manager.save()
    assert redis_store.get(
        new_handler.session_manager.session_id).get("age", None) is None
