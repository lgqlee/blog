#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 09:03:09
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import tornado.gen
import providers.db


mongo_coll = providers.db.get("mongo").tags


@tornado.gen.coroutine
def findOrCreate(name):
    """
    根据标签名称返回标签的 id
    """
    info = {"name": name}
    tag = yield mongo_coll.find_one(info, projection={"name": False})
    if tag:
        return tag["_id"]
    tag_id = yield mongo_coll.insert(info)
    return tag_id
