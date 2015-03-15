#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import motor

from config import database

# 私有变量
__redis_pool = redis.ConnectionPool(**database["redis"])
__mongo_client = motor.MotorClient(database["mongo"]).blog


def get_redis_connection():
    return redis.Redis(connection_pool=__redis_pool)


def get_mongodb_connection():
    return __mongo_client
