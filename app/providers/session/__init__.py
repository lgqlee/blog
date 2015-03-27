#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 14:25:13
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from session.manager import SessionManger
from session.store import RedisStore


def register(handler, store_type, **kwags):
    store = None
    if store_type == "redis":
        client = kwags["client"]
        store = RedisStore(client)
    if store:
        return SessionManger(handler, store, **kwags)
