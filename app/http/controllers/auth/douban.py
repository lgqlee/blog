#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 19:34:23
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import tornado.gen

from app.http.controllers import Controller, Route
from providers.oauth2.douban import DoubanOAuth2Mixin


@Route("/auth/douban")
class DoubanOAuth2LoginController(Controller, DoubanOAuth2Mixin):

    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(
                code=self.get_argument('code')
            )
            if not user:
                # todo 需要提示告诉用户验证失败
                return
            pass
            # todo 返回成功，并设为登录状态
        else:
            yield self.authorize_redirect(
                scopes=['douban_basic_common', 'community_basic_user']
            )
