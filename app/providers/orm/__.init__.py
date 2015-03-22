#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 21:59:45
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

"""
unique index readonly default column database protect

class Author(Model):
    email = StringField(unique=True, index=True)
    first_name = StringField()
    last_name = StringField()

    articles = has_many(Article)

    def initialize(self):
        self.index(("first_name", "last_name"), unique=True)

class Article(Model):
    private = BoolField(default=False)
    title = StringField()
    url = StringField(unique=True, index=True)

    user = belongs_to(Author)
    # tags = has_some(Tag)

    @validate("title")
    def check_something(self, content)
        return ValidateError("something wrong")

    @before_hook("create")
    def on_create(self, article):
        pass

    @after_hook("create"):
    def after_create(self, article):
        pass

class Tag(Model):
    name = StringField()

    article = embedded_in(Article)
    # articles = has_many()

Author.create_article(title="some")
# Author.build_article(title="some")
# Author.aritcles.build() / .create()
"""
