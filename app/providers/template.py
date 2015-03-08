#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader


# 为 tornado 增加 jinja2 支持
class JinjaProvider(object):
    def __init__(self, template_path, **kwargs):
        self.template = None
        _kwargs = {
            "loader": FileSystemLoader(template_path),
        }
        _kwargs.update(kwargs)
        self.env = Environment(**_kwargs)

    def load(self, template_name):
        self.template = self.env.get_template(template_name)
        return self

    def generate(self, **kwargs):
        return self.template.render(**kwargs)