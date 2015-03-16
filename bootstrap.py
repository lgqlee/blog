#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 11:57:55
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import site
from inspect import getsourcefile
from os import path

"""
通过 .pth 文件将主要的路径都放入 sys.path
减少 import 的路径长度
"""

__current_module__ = path.dirname(path.abspath(getsourcefile(lambda _: None)))
site.addsitedir(path.join(__current_module__, "app"))
