#!/usr/bin/python
# -*- coding: utf-8 -*-

mongo = "mongodb://localhost/"
redis = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    # 阻止 redis 返回 byte 类型
    "decode_responses": True,
}
