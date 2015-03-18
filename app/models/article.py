#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 07:27:06
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com
from bson.objectid import ObjectId
import tornado.gen

import providers.db

"""
users collection
字段名称     数据类型    可空
title       string     no
email       string     no
password    string     yes
roles       string[]   yes
created_at  datetime   no
- - -
草稿使用单独的草稿库来存放
确认发布后再与原文章合并更新
"""

mongo_coll = providers.db.get("mongo").users
