#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from app.extended.jinja_loader import JinjaProvider


_env = os.environ.get("RUNTIME_ENV", "development")

app_config = {
    "env": _env,
    "debug": _env is not "production",
    "template_path": "./resources/views",
    "template_loader": JinjaProvider("./resources/views",
                                     auto_reload=_env is not "production"),
    "static_path": "./resources/assets",
    "xsrf_cookies": True,
    "cookie_secret": "yourSecretHere",
    "login_url": "/login",
}