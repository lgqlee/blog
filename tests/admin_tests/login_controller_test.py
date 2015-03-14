#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pymongo
import hashlib
from passlib.hash import sha256_crypt
from nose import with_setup

from config.database import mongo


def generate_password(password):
    m = hashlib.md5()
    m.update(password.encode("utf8"))
    return m.hexdigest()


test_email = "fake@fake.com"
test_pass = generate_password("123456")
coll = pymongo.MongoClient(mongo).blog.users


class LoginTest():
    def __init__(self):
        self._test_user_id = None

    def setup_func(self):
        self._test_user_id = coll.insert(
            {"email": test_email, "password": sha256_crypt.encrypt(test_pass), "roles": [], "name": "fake"})

    def teardown_func(self):
        coll.remove({"_id": self._test_user_id})


t = LoginTest()


@with_setup(setup=t.setup_func, teardown=t.teardown_func)
def login_tests():
    res = requests.post("http://localhost:8000/admin/login", {
        "email": test_email,
        "password": test_pass,
    })
    assert res.status_code == 200
    assert res.json()["code"] == 200


def login_error_tests():
    res = requests.post("http://localhost:8000/admin/login", {
        "email": test_email,
    })
    assert res.status_code == 400
    res = requests.post("http://localhost:8000/admin/login", {
        "email": test_email,
        "password": "-",
    })
    assert res.json()["code"] == 403
    res = requests.post("http://localhost:8000/admin/login", {
        "email": test_email + "-",
        "password": test_pass,
    })
    assert res.json()["code"] == 403