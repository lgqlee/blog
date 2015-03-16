#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-16 19:50:54
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _


from inspect import getsourcefile
from os import path
from app.providers import template

__current_module__ = path.dirname(path.abspath(getsourcefile(lambda _: None)))

jinja2_loader = template.use("jinja2", __current_module__)


def test_resolve_path():
    assert jinja2_loader.resolve_path(
        "template_example.txt", parent_path="test") == "template_example.txt"


def test_get_template():
    t = jinja2_loader._create_template("template_example.txt")
    assert t.generate(name="world") == "hello world"
