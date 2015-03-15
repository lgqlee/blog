#!/usr/bin/python
# -*- coding: utf-8 -*-

from controllers import Controller


class LogoutController(Controller):

    def get(self):
        self.logout()
        if not self.is_ajax:
            return self.redirect("/")
        self.write({"code": 200, "message": "logout success"})

    post = get
