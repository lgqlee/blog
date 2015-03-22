#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-22 16:22:22
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from .fields import *


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

        self.database = database
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
