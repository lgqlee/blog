#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 16:59:58
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com


import redis
import motor

from config import database

mongo_config = database["mongo"]
connection_pools = {
    "redis": redis.ConnectionPool(**database["redis"]),
    "mongo": motor.MotorClient(mongo_config["host"])[mongo_config["database"]]
}


def _get_redis_client():
    return redis.Redis(connection_pool=connection_pools["redis"])


def _get_mongo_client():
    return connection_pools["mongo"]


def get(name):
    return {
        "redis": _get_redis_client,
        "mongo": _get_mongo_client
    }[name]()
