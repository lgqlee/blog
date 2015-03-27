#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-17 18:14:53
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import requests
import bootstrap as _
from passlib.hash import sha256_crypt
from hashlib import md5
from pymongo import MongoClient

from config import database

mongo_config = database["mongo"]
coll = MongoClient(mongo_config["host"])[
    mongo_config["database"]].users


class UserTests():

    def setUp(self):
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

    def test_success_login(self):
        res = requests.post("http://localhost:8000/admin/login", {
            "email": self.tmp_email,
            "password": self.tmp_password,
        })
        assert res.status_code == 200
        assert res.json()["code"] == 200

    def test_params_error_login(self):
        res = requests.post("http://localhost:8000/admin/login", {
            "email": self.tmp_email,
        })
        assert res.status_code == 400

    def test_account_error_login(self):
        res = requests.post("http://localhost:8000/admin/login", {
            "email": self.tmp_email,
            "password": "-",
        })
        assert res.json()["code"] == 412
        res = requests.post("http://localhost:8000/admin/login", {
            "email": self.tmp_email + "a",
            "password": self.tmp_password,
        })
        assert res.json()["code"] == 412
