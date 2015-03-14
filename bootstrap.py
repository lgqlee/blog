#!/usr/bin/python
# -*- coding: utf-8 -*-

import site

"""
通过 .pth 文件将主要的路径都放入 sys.path
减少 import 的路径长度
"""
site.addsitedir("app")
