#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import url

from index_controller import IndexController
from auth.github_controller import GithubOAuth2LoginController
from auth.douban_controller import DoubanOAuth2LoginController
from admin.login_controller import AdminLoginController
from logout_controller import LogoutController
from admin.dashboard_index_controller import DashboardIndexController

routes = [
    url(r"/", IndexController),
    url(r"/auth/github", GithubOAuth2LoginController),
    url(r"/auth/douban", DoubanOAuth2LoginController),
    url(r"/logout", LogoutController),
    url(r"/admin/login", AdminLoginController),
    url("/admin", DashboardIndexController)
]
