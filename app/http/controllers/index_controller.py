#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.http.controllers import Controller


class IndexController(Controller):
    def get(self):
        self.session["name"] = "Vincent"
        self.render('index.html', name="world")