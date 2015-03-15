#!/usr/bin/python
# -*- coding: utf-8 -*-

from controllers import Controller


class DashboardIndexController(Controller):

    def get(self):
        self.render("admin/dashboard.html")
