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
    assert len(mo.get_fields()) is 2
    assert "age" in mo.get_field_names()

    other = IntField(default=noop)
    setattr(other, "name", "other")
    assert mo.get_field_index(other) is -1
    assert mo.get_field_index(name) > -1


def test_empty_model():
    try:
        Model()
        assert True
    except AttributeError:
        pass


def test_model_meta_class():
    class User(Model):

        class Meta(object):
            _t = 1
            t = 1

    u = User()
    assert u._meta.t == 1
    assert not hasattr(u._meta, "_t")


def test_model_attrs():
    class User(Model):
        name = StringField()
        age = IntField()

    vt = User()
    assert vt.is_dirty is False
    vt.name = "vincent"
    assert vt.is_dirty is True
    assert len(vt.dirty_fields) == 1


def test_sub_class():
    class User(Model):
        name = StringField()
        age = IntField(default=20)

    class Worker(User):
        name = StringField(default="none")
        job = IntField()

    vt = Worker()
    assert vt.age == 20
    assert vt.name  == "none"
