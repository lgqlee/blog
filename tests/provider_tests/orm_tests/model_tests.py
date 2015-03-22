#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-22 17:01:33
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _

from app.providers.orm.model import *


def test_model_options_default():
    def noop():
        return 1
    name = StringField(default="vincent")
    setattr(name, "name", "name")
    age = IntField(default=noop)
    setattr(age, "name", "age")
    mo = ModelOptions(list, ext=1)
    assert mo.ext is 1

    mo.fields = {"name": name, "age": age}
    mo.prepared()
    assert mo._default_callables[age] is noop
    assert mo._default_dict[name] == mo._default_by_name["name"]
    assert len(mo.get_field_names()) is 2
    assert "age" in mo.get_field_names()

    other = IntField(default=noop)
    setattr(other, "name", "other")
    assert mo.get_field_index(other) is -1
    assert mo.get_field_index(name) > -1
