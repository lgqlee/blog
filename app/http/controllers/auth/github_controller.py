#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.gen
from app.http.controllers import Controller
from extended.oauth.github import GithubOAuth2Mixin


class GithubOAuth2LoginController(Controller, GithubOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(code=self.get_argument('code'))
            if not user:
                # todo 需要提示告诉用户验证失败
                return
            pass
            # todo 返回成功，并设为登录状态
        else:
            yield self.authorize_redirect(scopes=['user:email'])