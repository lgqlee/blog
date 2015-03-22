#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 15:57:20
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from .jinja2 import JinjaLoader


def use(template, root_path, **kwargs):
    loader = {
        "jinja2": JinjaLoader
    }[template]
    return loader(root_path, **kwargs)
