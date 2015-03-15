#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 11:57:55
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from tornado.ioloop import IOLoop
from tornado.web import Application

import bootstrap as _
from route import routes
from config import app as config

app = Application(routes, **config)
app.listen(8000)

if __name__ == '__main__':
    IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    IOLoop.current().start()
