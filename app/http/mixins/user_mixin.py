#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
users
- - -
field: name,        type: string*
field: email,       type: string*
field: password,    type: string
field: roles,       type: []string
field: token,       type: string*
"""
from bson.objectid import ObjectId
import hashlib
import tornado.gen
import uuid
from passlib.hash import sha256_crypt


class UserMixin():
    USER_AUTH_COOKIE = "PHP_SESSION"
    SESSION_USER_INFO = ("name", "_id", "roles", "email")

    @tornado.gen.coroutine
    def _auth_password(self, email, password):
        user = yield self.conn.users.find_one({"email": email})
        return user and user["password"] and sha256_crypt.verify(password, user["password"]) and user

    @tornado.gen.coroutine
    def _check_auth_cookie(self):
        auth_cookie = self.get_secure_cookie(self.USER_AUTH_COOKIE, None)
        if not auth_cookie:
            return False
        (user_id, md5_str) = auth_cookie.decode("utf-8", "strict").split("|")
        if not md5_str:
            return False
        coll = self.conn.users
        user = yield coll.find_one({"_id": ObjectId(user_id)})
        if not user:
            return False
        m = hashlib.md5()
        m.update(
            ("{0}{1}".format(user["token"], self.request.headers["User-Agent"])).encode("utf8"))
        return m.hexdigest() == md5_str and user

    def _generate_auth_cookie(self, token):
        m = hashlib.md5()
        m.update(
            ("{0}{1}".format(token, self.request.headers["User-Agent"])).encode("utf8"))
        self.set_secure_cookie(self.USER_AUTH_COOKIE, "{0}|{1}".format(self.session["_id"], m.hexdigest()),
                               expires_days=365, httponly=True)

    @tornado.gen.coroutine
    def update_token(self, user):
        token = hashlib.sha256(str(uuid.uuid4()).encode("utf8")).hexdigest()
        result = yield self.conn.users.update({"_id": user["_id"]}, {"$set": {"token": token}})
        if result['n'] < 1:
            return False
        return token
