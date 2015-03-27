#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-16 08:41:25
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _

from app.providers.session.store import RedisStore
from app.providers import db

redis_client = db.get("redis")


def test_default_store():
    fake_id, fake_content = "this_is_a_test_id", "some text"
    redis_store = RedisStore(redis_client)
    redis_store.set(fake_id, fake_content)
    assert redis_client.get(
        "{0}:{1}".format(redis_store.DEFAULT_PREFIX, fake_id)) == fake_content
    assert redis_store.get(fake_id) == fake_content
    redis_store.set(fake_id, None)
    assert redis_store.dumps(None) == None


def test_custom_prefix_store():
    fake_id, fake_content = "this_is_a_test_id", "some text"
    custom_prefix = "s"
    custom_store = RedisStore(redis_client, prefix=custom_prefix)
    custom_store.set(fake_id, fake_content)
    assert redis_client.get(
        "{0}:{1}".format(custom_prefix, fake_id)) == fake_content
    custom_store.set(fake_id, None)
    assert redis_client.get(
        "{0}:{1}".format(custom_prefix, fake_id)) == None
