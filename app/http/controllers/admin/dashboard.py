#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 19:57:59
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from controllers import Controller


class DashboardIndexController(Controller):

    def get(self):
        self.render("admin/dashboard.html")
