#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 12:06:46
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import os
import toml

from providers import template

__env = os.environ.get("RUNTIME_ENV", "development")
__is_production = __env is "production"

with open("./config/app.toml") as conffile:
    app = toml.loads(conffile.read())[__env]
with open("./config/database.toml") as conffile:
    database = toml.loads(conffile.read())[__env]

"""
根据当前是否为生产环境生成部分配置
通过 `export RUNTIME_ENV=production` 来告知当前程toml序为生产环境
"""
print("server is now running in {0} mode".format(__env))

# 用户自定义与系统配置进行合并
app.update({
    "env": __env,
    "debug": __env is not "production",
    "template_path": "./resources{0}/views".format(
        __is_production and '/dist' or ''
    ),
    "template_loader": template.use("jinja2", "./resources/views",
                                    auto_reload=not __is_production),
    "static_path": "./static{0}".format(
        __is_production and '/dist' or ''
    ),
    "xsrf_cookies": __is_production,
})
