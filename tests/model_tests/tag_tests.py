#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 13:14:40
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _

from tornado.ioloop import IOLoop
from tornado.testing import AsyncTestCase
from tornado.testing import gen_test
from pymongo import MongoClient
from bson.objectid import ObjectId

from app.models import tag as Tag
from config import database

mongo_config = database["mongo"]
coll = MongoClient(mongo_config["host"])[
    mongo_config["database"]].tags


class UserTests(AsyncTestCase):
    FAKE_TAG = "这是一个测试的"

    def get_new_ioloop(self):
        return IOLoop.instance()

    def setUp(self):
        AsyncTestCase.setUp(self)

    # 测试完毕销毁账号
    def tearDown(self):
        coll.remove({
            "name": self.FAKE_TAG,
        })

    @gen_test
    def test_find_create(self):
        tag_id = yield Tag.findOrCreate(self.FAKE_TAG)
        assert isinstance(tag_id, ObjectId)
        new_tag_id = yield Tag.findOrCreate(self.FAKE_TAG)
        assert str(tag_id) == str(new_tag_id)
