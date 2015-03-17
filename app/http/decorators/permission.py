#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-17 21:18:31
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import functools
from tornado.web import HTTPError


def permission(*roles):
    """验证当前用户是否有权限执行该方法的装饰器
    @permission("admin")
    def get(self):
        pass
    如果未登录则根据是否 ajax 返回 json 或者跳转。
    已登录则查看权限是否满足，不满足直接返回 404
    """
    def _permission(next):
        @functools.wraps(next)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                # 如果是 ajax 请求，则返回 json
                if self.is_ajax:
                    return self.write({
                        "code": 403,
                        "message": "please login",
                    })
                if self.request.method in ("GET", "HEAD"):
                    self.redirect(self.get_login_url())
                    return
                raise HTTPError(403, reason="Please login")
            if len(roles) > 0:
                current_roles = self.current_user.get("roles", ())
                # 判断当前权限是否大于需要的权限，否则返回 404 错误
                if set(current_roles) < set(roles):
                    if self.is_ajax:
                        return self.write({
                            "code": 401,
                            "message": "permission denied",
                        })
                    raise HTTPError(404, reason="Page not found")
            return next(self, *args, **kwargs)
        return wrapper
    return _permission
