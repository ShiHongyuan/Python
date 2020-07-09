#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shihongyuan'

'''
对象关系模型

因为在基于协程的异步web框架中，不能调用普通的同步IO操作，必须是异步的IO操作

这就是异步编程的一个原则：一旦决定使用异步，则系统每一层都必须是异步，“开弓没有回头箭”。

幸运的是aiomysql为MySQL数据库提供了异步IO的驱动。

'''
import logging; logging.basicConfig(level=logging.INFO)

import asyncio
import aiomysql

def log(sql, args=()):
    logging.log(logging.INFO, 'SQL: %s', sql)

'''
创建连接池：提供可以复用的一直跟数据库连接上的连接，不用频繁与数据库打开和关闭连接

全局变量：__pool
'''
# async表示协程：协程是一个线程，但执行过程中，遇到IO转给系统调用后，可中断转而执行别的子程序，在适当的时候再返回来接着执行
# 在基于协程的异步web框架里，因为只有一个线程处理所有用户的请求，在某个请求等待async声明的协程去获取连接、执行sql、获取sql结果等返回的时候，当前线程会去执行其他用户的请求，等到返回再回来继续执行
# 实现协程的方式有两种：
# 1、@asyncio.coroutine修饰需要用到协程的函数 + yield from 函数里用到协程的地方
# 2、把@asyncio.coroutine替换为async、把yield from替换为await
async def create_pool(loop, **kw):
# async def create_pool(**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['database'],
        # 应该是utf8，而不是utf-8，否则会报错
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )



# args参数的类型是List
async def select(sql, args, size=None):
    log(sql, args)
    # global __pool
    # async with ... as(cur = yield from ...)将调用一个子协程（也就是在一个协程中调用另一个协程）并直接获得子协程的返回结果。
    # 注意这里用了async with，而不是await with，我也不知道为什么？
    async with __pool.get() as conn:
        # with所求值的对象必须有一个enter()方法，一个exit()方法，
        # 紧跟with后面的语句被求值后，返回对象的enter()方法被调用，这个方法的返回值将被赋值给as后面的变量。当with后面的代码块全部被执行完之后，将调用前面返回对象的exit()方法，
        # 在with后面的代码块抛出任何异常时，exit()方法也会被执行
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # 坚持使用带参数的SQL，而不是自己拼接SQL字符串，这样可以防止SQL注入攻击
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs


# 要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的execute()函数
# args参数的类型是List
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected


# # 等同于上面
# @asyncio.coroutine
# def select(sql, args, size=None):
#     log(sql, args)
#     global __pool
#     with (yield from __pool) as conn:
#         cur = yield from conn.cursor(aiomysql.DictCursor)
#         yield from cur.execute(sql.replace('?', '%s'), args or ())
#         if size:
#             rs = yield from cur.fetchmany(size)
#         else:
#             rs = yield from cur.fetchall()
#         yield from cur.close()
#         logging.info('rows returned: %s' % len(rs))
#         return rs
#
# # 等同于上面
# @asyncio.coroutine
# def execute(sql, args):
#     log(sql)
#     with (yield from __pool) as conn:
#         try:
#             cur = yield from conn.cursor()
#             yield from cur.execute(sql.replace('?', '%s'), args)
#             affected = cur.rowcount
#             yield from cur.close()
#         except BaseException as e:
#             raise
#         return affected



'''
工具函数：为生成sql时拼装指定个数的占位符服务
'''
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)



# 保存数据库表的字段名和字段类型，表的字段名与定义的User类的属性名不一定一样
class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        # 该字段在表中的字段名
        self.name = name
        # 该字段在表中的类型
        self.column_type = column_type
        # 该字段是否是主键
        self.primary_key = primary_key
        # 该字段的默认值，不是用户定义的默认值，是表字段自己的默认值
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar'):
        super().__init__(name, ddl, primary_key, default)


class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'float', primary_key, default)


class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)






# cls表示自身类，self表示自身实例
# 通过__init__的self绑定的是实例属性，其他的是类属性，类属性所有实例都能访问，而且修改后，其它实例也会影响，但是在访问同名的实例属性时，类属性会隐藏
# __xxx__方法是实例的特殊方法，不同于普通方法的调用方式，会被隐形自动调用，如创建实例时__init__()、x.y获取属性时调用__getattr__()
# __xxx__属性是类或者实例的特殊属性，存放着类的内置属性，以及随着实例的创建而创建一些属性
# 私有属性：_xxx 或者 __xxx

# metaclass是类的模板，所以必须从`type`类型派生：
class ModelMetaclass(type):

    # __new__()方法接收到的参数依次是：
    # 当前准备创建的类自身.
    # 类的名字.
    # 类继承的父类集合.
    # 类的方法集合.
    def __new__(cls, name, bases, attrs):
        # 排除model类自身，不改变model类的属性
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table名字，table定义为类属性
        # 如果没有获取到table属性，以类名作为表名
        # dict获取值方式dict.get(key)
        # get(key, default), 默认值不是None，tablename为默认值，默认值是None，tablename则为name
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        # 获取所有的对象属性和表字段的映射:
        mappings = dict()
        # 表字段(不包括主键)
        fields = []
        # 表的主键字段
        primaryKey = None
        # 模型的自定义字段
        modelFields = []
        # 模型的自定义主键字段
        modelPrimaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info(' found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = getattr(v, 'name', None) or k
                    modelPrimaryKey = k
                else:
                    fields.append(getattr(v, 'name', None) or k)
                    modelFields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        # 如果找到一个Field属性，就把它保存到一个__mappings__的dict中，同时从类属性中删除该Field属性，否则，容易造成运行时错误（实例的属性会遮盖类的同名属性）：
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))

        # 保存属性和列的映射关系，这里保存的都是类属性
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        # 主键属性名
        attrs['__primary_key__'] = primaryKey
        # 除主键外的属性名
        attrs['__fields__'] = fields

        # 模型自定义的属性
        attrs['__model_fields__'] = modelFields
        attrs['__model_primary_key__'] = modelPrimaryKey


        # 构造默认的SELECT, INSERT, UPDATE和DELETE语句：
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)



# 任何继承自Model的类（比如User），会自动通过ModelMetaclass扫描映射关系，并存储到自身的类属性如__table__、__mappings__中

# Model从dict继承，所以具备所有dict的功能，同时又实现了特殊方法__getattr__()和__setattr__()，因此又可以像引用普通字段那样写：
# user['id']  ok
# user.id     ok
# 注意到Model只是一个基类，如何将具体的子类如User的映射信息读取出来呢？答案就是通过metaclass：ModelMetaclass
# getattr()和setattr()方法是基类object的自带方法，每个对象都有；dict也有getattr()和setattr()方法，但是不能从他们获取dict的值，因为dict的值不属于它的一般属性

# Python解释器在创建Model类的时候，要通过ModelMetaclass.__new__()来创建，在此，我们可以修改类的定义
class Model(dict, metaclass=ModelMetaclass):

    # 可变参数：参数对象是list或者tuple，参数是没有指定参数名的
    # 定义和读取：
    # def calc(*args):
    #   for n in args
    # 使用传参：
    # nums = [1, 2, 3]
    # calc(*nums)  或者 calc(nums[0], nums[1], nums[3]) 或者 calc(1, 2, 3)
    #
    # 关键字参数：参数对象是dict，参数必须指定参数名
    # 定义和读取：
    # def person(**kw):
    #   city = kw['city']
    # 使用参数：
    # extra = {'city': 'Beijing', 'job': 'Engineer'}
    # person(**extra) 或者 person(city=extra['city'], job=extra['job']) 或者 person(city='Beijing', job='Engineer')
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    # user.id 自己会去调用__getattr__方法，等价于user.__getattr__(id)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # user.id = 1 自己会去调用__setattr__方法，等价于user.__setattr__(id, 1)
    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        # getattr(x, 'y') is equivalent to x.y，也是会自己去调__getattr__方法
        return getattr(self, key, None)

    # 如果用户没有设置字段的值，就用字段的默认值
    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                # 缺省值可以作为函数对象传入，在调用save()时自动计算，比如：随机id和当前时间
                # id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
                # created_at = FloatField(default=time.time)
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                # setattr(x, 'y', v) is equivalent to ``x.y = v''
                setattr(self, key, value)
        return value



    # 往Model类添加class方法，就可以让所有子类调用class方法：
    # classmethod修饰符：对应的函数是类方法，不是实例方法，不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等，只能被类调用
    # @staticmethod修饰符：同static方法，不需要self参数，也不需要cls参数，可以被类调用，也可以被实例调用
    # 普通方法：实例的方法，需要self参数，只能被实例调用

    # 使用：User.findAll()
    # args的类型是List
    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        # 调用类属性
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                # extend()方法只接受一个列表作为参数，并将该参数的每个元素都添加到原有的列表中
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        # select方法的args参数也是List
        rs = await select(' '.join(sql), args)
        # 返回cls[**r]是一个User对象的List
        return [cls(**r) for r in rs]

    # 根据主键查找某一条记录
    @classmethod
    async def findById(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    # 获取某个字段的数据库记录条数
    # num = yield from User.findNumber('count(id)')
    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        # _num_ 是count(id)的别名
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    # 实例方法
    async def save(self):
        # map()返回一个Iterator，迭代对象是惰性序列，需要用list()生成一个列表
        # 保存可以实例化时不设置值，保存默认值
        args = list(map(self.getValueOrDefault, self.__model_fields__))
        args.append(self.getValueOrDefault(self.__model_primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def update(self):
        # 修改是已经保存过一次了，没有值的在保存的时候都赋予了值，所以self.getValue不会报错，这个命令只是修改需要修改的，通过user.name='shy';user.update();使用
        args = list(map(self.getValue, self.__model_fields__))
        args.append(self.getValue(self.__model_primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__model_primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)



























