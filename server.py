#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 11:57:55
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import define, options, parse_command_line

import bootstrap as _
from route import routes
from config import app as config

define("port", default=8000, help="run on the given port", type=int)

if __name__ == '__main__':
    parse_command_line()
    app = Application(routes, **config)
    app.listen(options.port)
    IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    IOLoop.current().start()
