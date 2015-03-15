#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 15:27:02
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import random
import os

with open(os.path.join(__path__[0], "qoutes.txt")) as f:
    qoutes = f.readlines()


def rand():
    return random.choice(qoutes)
