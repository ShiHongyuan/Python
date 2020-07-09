#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shihongyuan'

'''
数据库对象模型
Models for user, blog, comment.
'''

import time, uuid
from orm import Model, StringField, BooleanField, FloatField, TextField


# 利用uuid生成随机id
def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    # 当对象定义的属性名和表字段名一样时，就不需要定义Field的name，就默认None，会把属性名当做字段名
    # 缺省值可以作为函数对象传入，在调用save()时自动计算
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    # 缺省值可以作为函数对象传入，在调用save()时自动计算
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'blogs'

    # 缺省值可以作为函数对象传入，在调用save()时自动计算
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(50)')
    # 标题
    name = StringField(ddl='varchar(50)')
    # 摘要
    summary = StringField(ddl='varchar(50)')
    # 内容
    content = TextField()
    # 缺省值可以作为函数对象传入，在调用save()时自动计算
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'comments'

    # 缺省值可以作为函数对象传入，在调用save()时自动计算
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    # 缺省值可以作为函数对象传入，在调用save()时自动计算
    created_at = FloatField(default=time.time)








