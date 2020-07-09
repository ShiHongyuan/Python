#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shihongyuan'

'''
users表的对象模型User
'''
# import www.orm
import logging; logging.basicConfig(level=logging.INFO)
# 飘红不管他，在同一个包下可以直接引用，不用加包名，也能找到
from orm import Model, StringField, IntegerField, create_pool
import asyncio


class User(Model):
    __table__ = 'users'

    # id = IntegerField('id', primary_key=True)
    # name = StringField('name', ddl='varchar(50)')

    id = IntegerField(primary_key=True)
    name = StringField(ddl='varchar(50)')

    def __str__(self):
        # 用self.getValue(k)就可以，用self.k就不行，会报错找不到那个key
        # 我觉得我有点知道了：因为初始化的时候，id和name是对象User的属性，是通过setattr()方法设置的属性，但是不是字典user['xxx']里面的属性，所以获取self.k会报错，只能通过getattr()去获取；
        # 但是当修改属性user.name = 'shihongyuan'，又是调用的__setattr__，就赋予了user['xxx']属性，可以通过这个获取，并且会覆盖以前通过setattr()方法设置的同名的属性，也可以通过getattr()获取最新的属性
        return '%s ==> %s' % (self.__class__.__name__, list(map(lambda k: self.getValueOrDefault(k), self.__model_fields__)))



# 测试
if  __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_pool(loop, host='127.0.0.1', port=3306, user='root', password='123456', db='awesome_python3'))
    user = User(id=112, name='Michael')
    logging.info(user)
    loop.run_until_complete(user.save())
    user.name = 'shihongyuan'
    loop.run_until_complete(user.update())
    loop.run_until_complete(user.remove())
    users = loop.run_until_complete(User.findAll())
    logging.info(users)
    for u in users:
        logging.info(u)
    # run_forever必须放在最后面才生效
    loop.run_forever()

    # asyncio.run(create_pool(host='127.0.0.1', port=3306, user='root', password='123456', db='awesome_python3'))

    # 创建实例:
    # user = User(id=233, name='Michael')

    # 存入数据库:
    # asyncio.run(user.save())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(create_pool(loop, host='127.0.0.1', port=3306, user='root', password='123456', db='awesome_python3'))
    # user = User(id=321, name='Michael')
    # loop.run_until_complete(user.save())
    # loop.run_forever()

    # 修改：
    # user.name = 'shihongyuan'
    # asyncio.run(user.update())

    # 查询此user对象:
    # 返回是一个User对象的List
    # user = User.find(123)
    # 查询所有User对象:
    # users = User.findAll()

    # 删除：
    # user.remove()

    # 查询所有User对象:
    # 返回是一个User对象的List
    # users = User.findAll()
