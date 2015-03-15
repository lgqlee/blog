#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 17:21:52
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from tornado.web import url

from controllers.index import IndexController
from controllers.auth.github import GithubOAuth2LoginController
from controllers.auth.douban import DoubanOAuth2LoginController
from controllers.admin.login import AdminLoginController
from controllers.logout import LogoutController
from controllers.admin.dashboard import DashboardIndexController

routes = [
    url(r"/", IndexController),
    url(r"/auth/github", GithubOAuth2LoginController),
    url(r"/auth/douban", DoubanOAuth2LoginController),
    url(r"/logout", LogoutController),
    url(r"/admin/login", AdminLoginController),
    url("/admin", DashboardIndexController)
]
