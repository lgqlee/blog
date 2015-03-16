#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 15:27:02
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import random
from inspect import getsourcefile
from os import path

__current_module__ = path.dirname(path.abspath(getsourcefile(lambda _: None)))

with open(path.join(__current_module__, "qoutes.txt")) as f:
    qoutes = f.readlines()


def rand():
    return random.choice(qoutes)
