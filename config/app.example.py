#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from app.providers.template import JinjaProvider


_env = os.environ.get("RUNTIME_ENV", "development")

app_config = {
    "env": _env,
    "debug": _env is "development",
    "template_path": "./resources/views",
    "template_loader": JinjaProvider("./resources/views",
                                     auto_reload=_env is "development"),
    "static_path": "./resources/assets",
    "xsrf_cookies": True,
    "cookie_secret": "",
    "login_url": "/login",
}