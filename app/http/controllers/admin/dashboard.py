#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 19:57:59
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from controllers import Controller, Route
from decorators.permission import permission


@Route("/admin")
class DashboardIndexController(Controller):

    @permission("admin")
    def get(self):
        self.render("admin/dashboard.html")
