#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-21 11:25:34
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

"""
定义了所有支持的字段类型
参考文档：http://api.mongodb.org/python/current/api/bson/son.html
"""

import re
from bson import ObjectId
from datetime import datetime


class FieldDescriptor(object):

    """
    提供描述符，直接提供给 model 使用
    """

    def __init__(self, field):
        self.field = field
        self.att_name = self.field.name

    def _is_readonly(self, instance):
        return instance and hasattr(instance, "readonly") and instance.readonly is True

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return instance._data.get(self.att_name, None)
        return self.field

    def __set__(self, instance, value):
        # 只读模式下，禁止修改
        if self._is_readonly(instance):
            raise AttributeError(
                "Can not change readonly attribute {0}".format(self.att_name))
        instance._data[self.att_name] = value
        # 通过记录原值来获得准确的修改值
        if instance._origin_data.get(self.att_name, None) == value:
            return instance._dirty.discard(self.att_name)
        instance._dirty.add(self.att_name)


class Field(object):

    """
     抽象类 Field
    """
    field_type = "field"

    def __init__(self, verbose_name=None, index=False, unique=False, readonly=False, default=None, column=None):
        self.index = index
        self.unique = unique
        self.readonly = readonly
        self.default = default
        self.column = column
        self.verbose_name = verbose_name

    @classmethod
    def extend(cls, name=None):
        def decorator(method):
            method_name = name or method.__name__
            setattr(cls, method_name, method)
            return method
        return decorator

    def add_to_class(self, model_class, name):
        """
        将数据绑定到 class，使用 FieldDescriptor 来实现 model 上对数据的读取与修改
        """
        self.name = name
        self.model_class = model_class
        self.column = self.column or self.name
        if not self.verbose_name:
            self.verbose_name = re.sub("_+", " ", name).title()

        model_class._meta.fields[self.name] = self
        model_class._meta.columns[self.column] = self
        # 为 model 绑定 FieldDescriptor 来操作 Field 的数据
        setattr(model_class, name, FieldDescriptor(self))

    def coerce(self, value):
        raise NotImplementedError()

    def db_value(self, value):
        return value if value is None else self.coerce(value)

    python_value = db_value


class BoolField(Field):
    field_type = "bool"
    coerce = bool


class IntField(Field):
    field_type = "int"
    coerce = int


class FloatField(Field):
    field_type = "float"
    coerce = float


class StringField(Field):
    field_type = "string"

    def coerce(self, value):
        if not value:
            return ""
        if isinstance(value, str):
            return value
        elif isinstance(value, bytes):
            return value.decode("utf-8")
        return str(value)


class ArrayField(Field):
    field_type = "array"
    coerce = list


class HashField(Field):
    field_type = "hash"
    coerce = dict


class DatetimeField(Field):
    field_type = "datetime"
    formats = [
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
    ]

    def coerce(self, value):
        if not isinstance(value, datetime):
            for fmt in self.formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    pass
        return value


class ObjectIdField(Field):
    field_type = "objectId"
    coerce = str

    def db_value(self, value):
        if isinstance(value, ObjectId):
            return value
        return ObjectId(value)


class BinaryField(Field):
    field_type = "binary"

    def coerce(self, value):
        if isinstance(value, bytes):
            return value
        return value.encode("utf-8")
