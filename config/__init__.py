#!/usr/bin/env python3
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

"""
开发环境中模板和静态文件分别存放在 ./resources/views 和 ./static
开发只需要维护 ./resources，./static 是 gulp setup 自动生成目录
同时他会根据 ./resources 的文件进行同步
发布时进行一些处理操作后放到 ./views 和 ./public 文件夹
"""
template_path = "./resources/views" if not __is_production else "./views"
static_path = "./static" if not __is_production else './public'

# 用户自定义与系统配置进行合并
app.update({
    "env": __env,
    "debug": __env is not "production",
    "template_loader": template.use("jinja2", template_path,
                                    auto_reload=not __is_production),
    "static_path": "./static{0}".format(
        __is_production and '/dist' or ''
    ),
    "xsrf_cookies": __is_production,
})
