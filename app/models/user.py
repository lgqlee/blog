#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 18:24:42
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from bson.objectid import ObjectId
import hashlib
import tornado.gen
import uuid
from passlib.hash import sha256_crypt

import providers.db

"""
users collection
字段名称    数据类型    可空
name       string     no
email      string     no
password   string     yes
roles      string[]   yes
token      string     no
"""
mongo_coll = providers.db.get("mongo").users

USER_INFO = ("name", "_id", "roles", "email")


def __user_info_filter(user):
    """
    过滤用户信息，如果是 ObjectId 转成 string
    """
    return {
        item: str(user[item]) if isinstance(user[item], ObjectId) else user[item]
        for item in user if item in user
    }


@tornado.gen.coroutine
def auth_by_password(email, password):
    """
    更具邮箱和密码进行账号认证
    认证成功返回详情
    """
    user = yield mongo_coll.find_one({"email": email})
    return user and user["password"] and sha256_crypt.verify(password, user["password"]) and __user_info_filter(user)


@tornado.gen.coroutine
def update_token(user_id):
    """
    根据用户 ID 更新用户验证 token
    如果生成失败返回 False
    """
    b_id = user_id if isinstance(user_id, ObjectId) else ObjectId(user_id)
    token = hashlib.sha256(str(uuid.uuid4()).encode("utf8")).hexdigest()
    result = yield mongo_coll.update({"_id": b_id}, {"$set": {"token": token}})
    if result['n'] < 1:
        return None
    return token


def encrypt_by_token(token, salt):
    """
    根据 token 将盐值进行加密处理
    """
    m = hashlib.md5()
    m.update(("{0}{1}".format(token, salt).encode("utf8")))
    return m.hexdigest()


@tornado.gen.coroutine
def check_token(user_id, salt, voucher):
    """
    根据用户 ID 验证经过 token 加密的盐值和凭证
    如果生成失败返回 False，否则返回用户信息
    """
    if not salt:
        return False
    b_id = user_id if isinstance(user_id, ObjectId) else ObjectId(user_id)
    user = yield mongo_coll.find_one({"_id": b_id})
    if not user:
        return False
    return encrypt_by_token(user["token"], salt) == voucher and __user_info_filter(user)
