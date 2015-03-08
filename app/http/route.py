#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import url
from app.http.controllers.index_controller import IndexController

routes = [
    url(r"/", IndexController),
]