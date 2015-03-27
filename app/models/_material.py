#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 18:12:23
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

"""
文章和草稿相同的字段如下：
title       string                no
content     dict{string: string}  yes
author      objectid              no
tags        objectid[]            no
deleted     boolean               yes
created_at  datetime              no
updated_at  datatime              no
- - -
相对于文章，草稿多了一个 article_id 字段
如果 article_id 为空则表示是一篇新文章，否则表示是一篇已经发布的文章的修改稿
"""


class Material(object):
    # 由于 文章和草稿绝大多数方法类似，所以使用统一的基类

    @staticmethod
    def get_coll():
        raise NotImplemented
