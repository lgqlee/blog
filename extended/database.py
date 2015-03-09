#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import motor

import config.database as config

# 私有变量
__redis_pool = redis.ConnectionPool(**config.redis)
__mongo_client = motor.MotorClient(config.mongo)


def get_redis_connection():
    return redis.Redis(connection_pool=__redis_pool)


def get_mongodb_connection():
    return __mongo_client