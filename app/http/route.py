#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import url

from app.http.controllers.index_controller import IndexController
from app.http.controllers.auth.github_controller import GithubOAuth2LoginController
from app.http.controllers.auth.douban_controller import DoubanOAuth2LoginController
from app.http.controllers.admin.login_controller import AdminLoginController

routes = [
    url(r"/", IndexController),
    url(r"/auth/github", GithubOAuth2LoginController),
    url(r"/auth/douban", DoubanOAuth2LoginController),
    url(r"/admin/login", AdminLoginController)
]