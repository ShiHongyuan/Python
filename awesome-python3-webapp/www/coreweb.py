#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shihongyuan'

'''
自定义的一个web框架，可以复用，后续只需要编写简单的业务处理函数
aiohttp的web框架相对比较底层，Web框架的设计是完全从使用者出发，目的是让使用者编写尽可能少的代码。
简单的业务函数（参数是变量，不是request）还可以方便单元测试，不需要模拟一个request才能测试。
'''


import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from apis import APIError


# 装饰器的作用：给一个函数放上装饰器，装饰器相当于重新改造了这个函数，在执行这个函数前后可以添加各种东西，然后也执行这个函数，返回一个改造后的函数，执行的时候就执行这个新的函数

def get(path):
    '''
    定义get请求的处理函数的装饰器: @get('/path')
    :param path: get请求的path
    :return: 加上了装饰器的get请求处理函数
    '''
    def decorator(func):
        # 将返回的wraps新函数name依然是原函数的名字
        @functools.wraps(func)
        # *args, **kw 可以包含所有的参数形式了
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator


def post(path):
    '''
        定义get请求的处理函数的装饰器: @post('/path')
        :param path: post请求的path
        :return: 加上了装饰器的post请求处理函数
        '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


def get_required_kw_args(fn):
    '''
    获取处理函数的请求参数（没有默认值的命名关键字参数）
    '''
    args = []
    # 模块提供了一些有用的函数帮助获取对象的信息，例如模块、类、方法、函数、回溯、帧对象以及代码对象。例如它可以帮助你检查类的内容，获取某个方法的源代码，取得并格式化某个函数的参数列表，或者获取你需要显示的回溯的详细信息。
    # 该模块提供了4种主要的功能：类型检查、获取源代码、检查类与函数、检查解释器的调用堆栈。
    # inspect.signature(fn)获取这个函数的所有签名属性
    # 位置参数：POSITIONAL_ONLY
    # 可变参数：VAR_POSITIONAL
    # 关键字或位置参数：POSITIONAL_OR_KEYWORD
    # 关键字参数：KEYWORD_ONLY：
    # 命名关键字参数: VAR_KEYWORD
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        # param.kind: 参数类型
        # KEYWORD_ONLY: 没有默认值的命名关键字参数，Value must be supplied as a keyword argument. Keyword only parameters are those which appear after a * or *args entry in a Python function definition.
        # empty: 没有默认值的参数
        # all keyword-only arguments without default values:获取没有默认值的命名关键字参数
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)


def get_named_kw_args(fn):
    '''
    获取处理函数的全部命名关键字参数
    '''
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        # 获取所有参数
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


def has_named_kw_args(fn):
    '''
    判断处理函数是否有命名关键字参数
    '''
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True


def has_var_kw_arg(fn):
    '''
    判断处理函数是否有关键字参数**kw
    :param fn:
    :return:
    '''
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        # VAR_KEYWORD: 关键字参数。A dict of keyword arguments that aren't bound to any other parameter. This corresponds to a **kwargs parameter in a Python function definition.
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True


def has_request_arg(fn):
    '''
    判断处理函数是否有request这个参数，并且是否是最后一个参数，如果request不是最后一个参数，会报错
    '''
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found


class RequestHandler(object):
    '''
    请求的处理函数不一定是一个coroutine，因此我们用RequestHandler()来封装一个统一的处理函数
    RequestHandler目的就是从请求的处理函数中分析其需要接收的参数，从request中获取必要的参数，调用处理函数，然后把结果转换为web.Response对象，从而构造成一个异步web的框架
    需要注册web应用的app和处理函数fn
    '''

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)


    # 定义__call__函数，可以将其实例视为函数
    async def __call__(self, request):
        kw = None
        # 如果处理函数有任意的参数，获取request的请求参数，并以字典的形式放到kw中
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':
                if request.method == 'POST':
                    # post请求没有请求体，报错
                    if not request.content_type:
                        return web.HTTPBadRequest('Missing Content-Type.')
                    ct = request.content_type.lower()
                    # 请求体转换格式错误，报错
                    if ct.startswith('application/json'):
                        params = await request.json()
                        if not isinstance(params, dict):
                            return web.HTTPBadRequest('JSON body must be object.')
                        kw = params
                    elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                        params = await request.post()
                        kw = dict(**params)
                    else:
                        # 无法处理的请求体格式，报错
                        return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
                if request.method == 'GET':
                    qs = request.query_string
                    if qs:
                        kw = dict()
                        # urllib的parse可以转换get的请求参数为键值对
                        for k, v in parse.parse_qs(qs, True).items():
                            kw[k] = v[0]
        # 如果kw为None,说明request请求体没有请求参数
        if kw is None:
            kw = dict(**request.match_info)
        # 如果kw不为None，说明request请求参数不为空，就把request的请求参数映射到处理函数的关键字参数上
        else:
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                # kw变成处理函数的参数，参数值是request的请求值
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
            # check required kw:
        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        # 用request的请求参数构成的kw作为参数，传递给处理函数，并执行处理函数，返回结果
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)


def add_static(app):
    '''
    通过app.router.add_static给web框架添加静态资源的路径，path为static下的资源
    '''
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))


def add_route(app, fn):
    '''
    通过app.router.add_route给web框架添加请求路径与处理函数之间的关系，有点像拦截器的作用
    '''
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    # 对于类型是method的，请求路径是path的请求，由RequestHandler去执行处理函数fn，并返回执行的结果
    app.router.add_route(method, path, RequestHandler(app, fn))


def add_routes(app, module_name):
    '''
    指定一个模块里的所有被@get或者@post修饰的处理函数都添加请求路径与处理函数之间的映射，就是web框架的添加路由的作用
    请求的处理函数就全部定义在一个module里，然后一次性给这个module添加路由就行了
    '''
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue

        fn = getattr(mod, attr)
        if callable(fn):
            logging.info(fn)
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                logging.info(fn)
                add_route(app, fn)












