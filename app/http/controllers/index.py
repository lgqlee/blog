#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 18:37:09
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from controllers import Controller


class IndexController(Controller):

    def get(self):
        self.render('index.html', name="world")
