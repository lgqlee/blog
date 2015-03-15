#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools

from tornado.concurrent import return_future
from tornado.auth import _auth_return_future, AuthError
from tornado import httpclient
from tornado.httputil import url_concat
from tornado import escape

try:
    import urllib.parse as urllib_parse
except ImportError:
    import urllib as urllib_parse


class DoubanOAuth2Mixin(object):
    _OAUTH_AUTHORIZE_URL = "https://www.douban.com/service/auth2/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://www.douban.com/service/auth2/token"
    _OAUTH_USER_BASE_URL = "https://api.douban.com/v2"
    _OAUTH_SETTINGS_KEY = "douban_oauth"

    @return_future
    def authorize_redirect(self, scopes=None, response_type="code", callback=None, **kwargs):
        args = {
            "client_id": self.settings[self._OAUTH_SETTINGS_KEY]["key"],
            "response_type": response_type,
            "redirect_uri": self.settings[self._OAUTH_SETTINGS_KEY]["redirect"]
        }
        if kwargs:
            args.update(kwargs)
        if scopes:
            args["scope"] = ",".join(scopes)
        self.redirect(
            url_concat(self._OAUTH_AUTHORIZE_URL, args))
        callback()

    @_auth_return_future
    def get_authenticated_user(self, code, callback, grant="authorization_code"):
        """Handles the login for the Github user, returning a user object.

        Example usage::

            class GithubOAuth2LoginHandler(tornado.web.RequestHandler,
                                           GithubOAuth2Mixin):
                @tornado.gen.coroutine
                def get(self):
                    if self.get_argument("code", False):
                        user = yield self.get_authenticated_user(code=self.get_argument("code"))
                        # Save the user with e.g. set_secure_cookie
                    else:
                        yield self.authorize_redirect(scope=["user:email"])
        """
        http = self.get_auth_http_client()
        body = urllib_parse.urlencode({
            "code": code,
            "client_id": self.settings[self._OAUTH_SETTINGS_KEY]["key"],
            "client_secret": self.settings[self._OAUTH_SETTINGS_KEY]["secret"],
            "redirect_uri": self.settings[self._OAUTH_SETTINGS_KEY]["redirect"],
            "grant_type": grant
        })

        http.fetch(self._OAUTH_ACCESS_TOKEN_URL,
                   functools.partial(self._on_access_token, callback),
                   method="POST",
                   headers={
                       "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
                   body=body)

    def _on_access_token(self, future, response):
        """Callback function for the exchange to the access token."""
        if response.error:
            future.set_exception(
                AuthError("Github auth error: %s" % str(response)))
            return

        args = escape.json_decode(escape.native_str(response.body))
        access_token = args.get("access_token", None)
        if not access_token:
            return future.set_result(None)
        self.douban_request(
            path="/user/~me",
            callback=functools.partial(
                self._on_get_user_info, future, access_token),
            access_token=access_token
        )

    @staticmethod
    def _on_get_user_info(future, access_token, user):
        if user is None:
            future.set_result(None)
            return
        user.update({"access_token": access_token})
        future.set_result(user)

    @_auth_return_future
    def douban_request(self, path, callback, access_token=None, post_args=None, **args):
        url = self._OAUTH_USER_BASE_URL + path
        all_args = {}
        all_args.update(args)
        if all_args:
            url += "?" + urllib_parse.urlencode(all_args)
        callback = functools.partial(self._on_douban_request, callback)
        http = self.get_auth_http_client()
        ua = "tornado"
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback, user_agent=ua,
                       headers={"Content-Type": "application/x-www-form-urlencoded",
                                "Authorization": "Bearer " + access_token, "Accept": "application/json"})
        else:
            http.fetch(url, method="GET", callback=callback, user_agent=ua,
                       headers={"Authorization": "Bearer " + access_token, "Accept": "application/json"})

    @staticmethod
    def _on_douban_request(future, response):
        if response.error:
            future.set_exception(AuthError("Error response %s fetching %s" %
                                           (response.error, response.request.url)))
            return

        future.set_result(escape.json_decode(response.body))

    @staticmethod
    def get_auth_http_client():
        return httpclient.AsyncHTTPClient()
