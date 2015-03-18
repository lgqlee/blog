#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-16 20:04:46
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _
from passlib.hash import sha256_crypt
from hashlib import md5
from tornado.ioloop import IOLoop
from tornado.testing import AsyncTestCase
from tornado.testing import gen_test
from pymongo import MongoClient

from app.models import user as User
from config import database

mongo_config = database["mongo"]
coll = MongoClient(mongo_config["host"])[
    mongo_config["database"]].users


class UserTests(AsyncTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def setUp(self):
        AsyncTestCase.setUp(self)
        self.tmp_email = "fake@fake.com"
        self.tmp_password = "121231"
        self.tmp_roles = ["admin"]
        self._create_user()

    # 生成一个临时的账号
    def _create_user(self):
        m = md5()
        m.update(self.tmp_password.encode(encoding='utf_8', errors='strict'))
        self.tmp_password = m.hexdigest()
        self.user_id = coll.insert({
            "name": "vt",
            "password": sha256_crypt.encrypt(self.tmp_password),
            "role": self.tmp_roles,
            "email": self.tmp_email
        })

    # 测试完毕销毁账号
    def tearDown(self):
        coll.remove({
            "name": "vt",
        })

    @gen_test
    def test_user_find(self):
        user = yield User.auth_by_password(
            self.tmp_email,
            self.tmp_password
        )
        assert user is not None

    @gen_test
    def test_user_token(self):
        token = yield User.update_token(self.user_id)
        assert token is not None

    @gen_test
    def test_token_from_wrong_id(self):
        token = yield User.update_token("0123456789ab0123456789ab")
        assert token is None

    @gen_test
    def test_get_user_info(self):
        user = yield User.info_by_id(self.user_id)
        assert user["name"] == "vt"

    @gen_test
    def test_token_check(self):
        token = yield User.update_token(self.user_id)
        voucher = User.encrypt_by_token(token, "here is salt")
        true_result = yield User.check_token(
            self.user_id, "here is salt", voucher)
        assert true_result is not False
        false_result = yield User.check_token(
            self.user_id, "here is fake salt", voucher)
        assert false_result is False
        false_result = yield User.check_token(
            self.user_id, "here is salt", "here is a fake voucher")
        assert false_result is False
        false_result = yield User.check_token(
            self.user_id, None, "here is a fake voucher")
        assert false_result is False
        false_result = yield User.check_token(
            "0123456789ab0123456789ab", "here is salt", "here is a fake voucher")
        assert false_result is False
