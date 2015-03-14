#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.http.controllers import Controller


class IndexController(Controller):

    def get(self):
        self.render('index.html', name="world")
