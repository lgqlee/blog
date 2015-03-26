#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 19:34:03
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from controllers import Controller, Route

@Route("/logout")
class LogoutController(Controller):

    def get(self):
        self.logout()
        if not self.is_ajax:
            return self.redirect("/")
        self.write({"code": 200, "message": "logout success"})

    post = get
