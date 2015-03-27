#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 06:41:13
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _
from tornado.web import HTTPError

from app.http.decorators.permission import permission

LOGIN_URL = "login"
REDIRECT_STATUS = "redirect"
NORMAL_STATUS = "normal"


def create_fake_handler(roles, **kwargs):

    class FakeRequest():

        def __init__(self, **kwargs):
            self.kwargs = kwargs

        @property
        def method(self):
            return self.kwargs.get("method", "GET")

    class FakeHandler(object):

        def __init__(self, **kwargs):
            self.current_user = kwargs.get("current_user", None)
            self.is_ajax = kwargs.get("is_ajax", False)
            self.request = FakeRequest(
                method=kwargs.get("request_method", "GET"))

        @permission(*roles)
        def target(self):
            return NORMAL_STATUS

        def get_login_url(self):
            return LOGIN_URL

        def redirect(self, url):
            return "{0}:{1}".format(REDIRECT_STATUS, LOGIN_URL)

        def write(self, msg):
            return msg

    return FakeHandler(**kwargs)


def test_permission_meet():
    handler = create_fake_handler(["admin", "comment"], current_user={
        "roles": ["admin", "comment", "author"]
    })
    assert handler.target() == NORMAL_STATUS


def test_not_login_get():
    handler = create_fake_handler(["admin", "comment"])
    assert handler.target() == "{0}:{1}".format(REDIRECT_STATUS, LOGIN_URL)


def test_not_login_ajax():
    handler = create_fake_handler(["admin", "comment"], is_ajax=True)
    assert handler.target()["code"] == 403


def test_permission_denied_ajax():
    handler = create_fake_handler(["admin", "comment"], is_ajax=True, current_user={
        "roles": ["comment"]
    })
    assert handler.target()["code"] == 401


def test_permission_denied_others():
    handler = create_fake_handler(["admin", "comment"], current_user={
        "roles": ["comment"]
    })
    try:
        handler.target()["code"]
        assert False
    except HTTPError as e:
        assert e.status_code == 404
