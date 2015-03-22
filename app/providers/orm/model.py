#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-22 16:22:22
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from copy import deepcopy

from .fields import *
from .query import *

DEFAULT_DATABASE = [None]


def set_database(database):
    # 修改 module 中的默认数据库
    DEFAULT_DATABASE[0] = database


class ModelOptions(object):

    def __init__(self, cls, database=None, db_collection=None, ** kwargs):
        self.model_class = cls
        self.name = cls.__name__.lower()
        self.fields = {}
        self.columns = {}
        self.defaults = {}
        self._default_by_name = {}
        self._default_dict = {}
        self._default_callables = {}

        self.database = database or DEFAULT_DATABASE[0]
        self.db_collection = db_collection

        for key, value in kwargs.items():
            setattr(self, key, value)
        self._additional_keys = set(kwargs.keys())

    def prepared(self):
        for field in self.fields.values():
            if field.default is not None:
                self.defaults[field] = field.default
                if callable(field.default):
                    self._default_callables[field] = field.default
                else:
                    self._default_dict[field] = field.default
                    self._default_by_name[field.name] = field.default

    def get_sorted_fields(self):
        return sorted(self.fields.items())

    def get_field_names(self):
        return [f[0] for f in self.get_sorted_fields()]

    def get_fields(self):
        return [f[1] for f in self.get_sorted_fields()]

    def get_field_index(self, field):
        for i, (field_name, field_obj) in enumerate(self.get_sorted_fields()):
            if field_name == field.name:
                return i
        return -1

    def get_default_dict(self, data):
        dd = self._default_by_name.copy()
        if self._default_callables:
            for field, default in self._default_callables.items():
                dd[field.name] = default()
        for field, value in data.items():
            dd[field] = value
        return dd


class BaseModel(type):

    def __new__(cls, name, bases, attrs):
        if not bases:
            return super(BaseModel, cls).__new__(cls, name, bases, attrs)

        meta_options = {}
        meta = attrs.pop('Meta', None)
        if meta:
            # 将 Meta 中所有的非私有属性全部带出
            for k, v in meta.__dict__.items():
                if not k.startswith('_'):
                    meta_options[k] = v

        for b in bases:
            if not hasattr(b, '_meta'):
                continue
            base_meta = getattr(b, '_meta')
            for (k, v) in base_meta.__dict__.items():
                # TODO 考虑继承父类的 meta_options
                pass
            for (k, v) in b.__dict__.items():
                if k in attrs:
                    # 父类不能覆盖子类的内容
                    continue
                if isinstance(v, FieldDescriptor):
                    # 继承父类的 field, 排除掉 _id，以及 updated_at 和 ignored_at
                    if not v.field.primary_key and not v.field.timestamp:
                        attrs[k] = deepcopy(v.field)

        # 初始化类并加上方法
        cls = super(BaseModel, cls).__new__(cls, name, bases, attrs)
        cls._meta = ModelOptions(cls, **meta_options)
        cls._data = None
        # 初始化 collection 名称
        if not cls._meta.db_collection:
            cls._meta.db_collection = re.sub(
                '[^\w]+', '_', cls.__name__.lower())

        # 找出所有的 Field 并使用 add_to_class 将他们绑定到当前 class
        fields = []
        for name, attr in cls.__dict__.items():
            if isinstance(attr, Field):
                fields.append((attr, name))
        # 默认添加 id 字段，必选
        fields.append((ObjectIdField(primary_key=True, column="_id"), "id"))
        # 如果没有 ignore_timestamp，添加 updated_at 和 created_at
        if not meta_options.get("ignore_timestamp", False):
            for f in ("created_at", "updated_at"):
                fields.append(
                    (ObjectIdField(timestamp=True), f))

        for field, name in fields:
            field.add_to_class(cls, name)
        cls._meta.prepared()

        if hasattr(cls, '__unicode__'):
            setattr(cls, '__repr__', lambda self: '<%s: %r>' % (
                cls.__name__, self.__unicode__()))
        return cls


class Model(metaclass=BaseModel):

    def __init__(self, data={}, **kwargs):
        self._data = self._meta.get_default_dict(data)
        self._origin_data = self._data.copy()
        self._dirty = set()
        self._obj_cache = {}

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def is_dirty(self):
        return bool(self._dirty)

    @property
    def dirty_fields(self):
        return [f for f in self._meta.get_fields() if f.name in self._dirty]

    @staticmethod
    @property
    def coll(cls):
        return cls._meta.database[cls._meta.db_collection]
