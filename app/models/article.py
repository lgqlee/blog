#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 07:27:06
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com
from bson.objectid import ObjectId
import tornado.gen

import providers.db

"""
aritcles collection
字段名称     数据类型               可空
title       string                no
content     dict{string: string}  yes
author      objectid              no
tags        objectid[]            no
deleted     boolean               yes
created_at  datetime              no
updated_at  datatime              no

- - -
drafts collection
字段名称     数据类型               可空
title       string                yes
article_id  objectid              yes
content     dict{string: string}  yes
author      objectid              no
tags        objectid[]            yes
deleted     boolean               yes
created_at  datetime              no
updated_at  datatime              no
"""
# 草稿使用单独的草稿库来存放
# 确认发布后再与原文章合并更新
