#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.http.controllers import Controller


class LogoutController(Controller):
    def get(self):
        self.logout()
        if not self.get_argument("ajax", False):
            self.redirect("/")
        self.write({"code": 200, "message": "logout success"})

    post = get