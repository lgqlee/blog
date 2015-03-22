#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-22 15:09:17
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import bootstrap as _

from datetime import datetime
from bson import ObjectId
from app.providers.orm.fields import *


def test_descriptor():
    origin_name = "vincent"

    class FakeField(object):
        name = "name"
        readonly = False

    class TestClass(object):
        d = FieldDescriptor(FakeField())

        _dirty = set()
        _origin_data = {"name": origin_name}
        _data = _origin_data.copy()

    m = TestClass()
    assert m.d == origin_name
    m.d = "othen name"
    assert "name" in m._dirty
    m.d = origin_name
    assert len(m._dirty) is 0


def test_sepicial_descriptor():
    class FakeField(object):
        name = "fake_name"
        readonly = True

    class TestClass(object):
        d = FieldDescriptor(FakeField())

        _dirty = set()
        _origin_data = {"name": "some name"}
        _data = _origin_data.copy()

    m = TestClass()
    try:
        m.d = "other"
        assert False
    except AssertionError:
        assert True
    assert isinstance(TestClass.d, FakeField)


def test_field():
    @Field.extend()
    def helo(self):
        return "helo"

    f = Field()
    assert f.helo() == "helo"


def test_bool_fields():
    b = BoolField()
    assert b.python_value(1) is True


def test_int_fields():
    i = IntField()
    assert i.python_value("1") is 1


def test_float_fields():
    f = FloatField()
    assert type(f.python_value(1)) is float


def test_string_fields():
    s = StringField()
    assert s.coerce(None) == ""
    assert s.coerce(b"helo") == "helo"
    assert s.coerce("helo") == "helo"
    assert s.coerce(True) == "True"


def test_array_fields():
    s = ArrayField()
    assert isinstance(s.coerce((1, 2, 3)), list)


def test_date_time_fields():
    s = DatetimeField()
    assert isinstance(s.coerce("1912-12-03"), datetime)
    assert isinstance(s.coerce(datetime.now()), datetime)


def test_object_id_fields():
    o = ObjectIdField()
    _id = o.db_value("550908800221b971526f24ab")
    assert isinstance(_id, ObjectId)
    assert _id is o.db_value(_id)
    assert o.python_value(_id) == str(_id)


def test_binary_fields():
    s = BinaryField()
    assert isinstance(s.coerce("hi"), bytes)
    assert s.coerce(b"hi") == b"hi"
