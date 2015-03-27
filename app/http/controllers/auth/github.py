#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-15 19:34:36
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import tornado.gen

from app.http.controllers import Controller, Route
from providers.oauth2.github import GithubOAuth2Mixin


@Route("/auth/github")
class GithubOAuth2LoginController(Controller, GithubOAuth2Mixin):

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
            yield self.authorize_redirect(scopes=['user:email'])
