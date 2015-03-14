#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from extended.jinja import JinjaLoader


_env = os.environ.get("RUNTIME_ENV", "development")
_is_production = _env is "production"

app_config = {
    "env": _env,
    "debug": _env is not "production",
    "template_path": "./resources{0}/views".format(_is_production and '/dist' or ''),
    "template_loader": JinjaLoader("./resources/views",
                                   auto_reload=not _is_production),
    "static_path": "./resources{0}/assets".format(_is_production and '/dist' or ''),
    "xsrf_cookies": _is_production,
    "cookie_secret": "",
    "login_url": "/admin_tests/login",
    "github_oauth": {
        "key": "",
        "secret": "",
    },
    "douban_oauth": {
        "key": "",
        "secret": "",
        "redirect": "http://yourwebsite.com/auth/douban"
    },
}
