#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application

import bootstrap as _
from route import routes
from config.app import app_config

app = Application(routes, **app_config)
app.listen(8000)

if __name__ == '__main__':
    IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    IOLoop.current().start()
