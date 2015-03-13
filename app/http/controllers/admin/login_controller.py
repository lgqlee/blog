#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.http.controllers import Controller
from extended.quotes import generate


class AdminLoginController(Controller):
    def get(self):
        self.render('admin/login.html', quote=generate())