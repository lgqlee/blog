#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-18 21:59:45
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

"""
unique index readonly default column database

class Author(Model):
    email = StringField(unique=True, index=True)
    first_name = StringField()
    last_name = StringField()

    index(("first_name", "last_name"), unique=True)
    articles = has_many(Article)
    # article = has_one(Article)

class Article(Model):
    private = BoolField(default=False)
    title = StringField()
    url = StringField(unique=True, index=True)

    user = belongs_to(Author)
    tags = embeds_many(Tag)
    # tag = embeds_one(Tag)

    @validate("title")
    def check_something(content)
        return ValidateError("something wrong")

    @before_hook("create")
    def on_create(article):
        pass

    @after_hook("create"):
    def after_create(article):
        pass

class Tag(Model):
    name = StringField()

    article = embedded_in(Article)

Author.create_article(title="some")
# Author.build_article(title="some")
# Author.aritcles.build() / .create()
"""
