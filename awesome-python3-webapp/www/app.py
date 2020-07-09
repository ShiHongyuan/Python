#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shihongyuan'

'''
async web application.  异步web应用， web app框架

Web框架使用了基于asyncio的aiohttp，这是基于协程的异步模型.
所有用户都是由一个线程服务的，协程的执行速度必须非常快，才能处理大量用户的请求。
而耗时的IO操作不能在协程中以同步的方式调用，否则，等待一个IO操作时，系统无法响应任何其他用户。
'''

import logging; logging.basicConfig(level=logging.INFO)

import os, json, time, asyncio
from datetime import datetime

from aiohttp import web
# 模板引擎: jinja2
from jinja2 import Environment, FileSystemLoader

import orm
from coreweb import add_routes, add_static
from handlers import cookie2user, COOKIE_NAME
from config import configs


'''
不用web框架时，只用urllib的web来处理请求
'''
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', headers={'content-type':'text/html'})


'''
web框架的内容
'''
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    # 不传入模板的path路径，就默认为：工程目录/templates
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    # 根据path加载模板文件
    env = Environment(loader=FileSystemLoader(path), **options)
    # 如果有传入filter条件，就给模板添加filter，让模板拥有一些自定义的功能函数
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    # 应用的__templating__属性存放模板文件
    app['__templating__'] = env

# 注册middleware拦截器的函数，把通用的日志功能从每个URL处理函数中拿出来，集中放到一个地方
async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        return (await handler(request))
    return logger


# 对于每个URL处理函数，如果我们都去写解析cookie的代码，那会导致代码重复很多次。
# 利用middle在处理URL之前，把cookie解析出来，并将登录用户绑定到request对象上，这样，后续的URL处理函数就可以直接拿到登录用户：
async def auth_factory(app, handler):
    '''
    定义一个request的拦截器函数，拦截请求，验证cookie是否是有效的，有效的会让request的__user__属性为请求的用户user，不是有效的就是None
    '''
    async def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        # 如果是第一次注册，就不会有cookie，cookie_str为空，就不会走校验，直接转给注册处理函数解决
        cookie_str = request.cookies.get(COOKIE_NAME)
        # 把当前用户绑定到request上，并对URL /manage/users 进行拦截，只有管理员身份才能看到用户页面，不是的话就要先登录
        logging.info('shy>>>>>>>>>>>>>>>>>>>>>>>>>1')
        if cookie_str:
            logging.info('shy>>>>>>>>>>>>>>>>>>>>>>>>>2')
            user = await cookie2user(cookie_str)
            if user:
                logging.info('shy>>>>>>>>>>>>>>>>>>>>>>>>>3')
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
                logging.info('shy>>>>>>>>>>>>>>>>>>>>>>>>>4' + request.__user__.name)
        if request.path.startswith('/manage/users') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')
        return (await handler(request))
    return auth



# 注册middleware拦截器的函数
async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))
    return parse_data


# 注册middleware拦截器的函数，把返回值转换为web.Response对象再返回，以保证满足aiohttp的要求
async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        # logging.info('shy>>>>>>>>>>>>>>>>>>>>>>>>>' + request.__user__)
        r = await handler(request)
        # stream类型的response不需要编码，本身就是流
        if isinstance(r, web.StreamResponse):
            return r
        # 字节类型的response也不需要编码
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        # str类型的response，是一个链接，需要编码后返回
        if isinstance(r, str):
            # 直接重定向
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        # 键值对类型的response，可能包含template页面，需要渲染模板，可能是纯api的json数据
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                # 如果是包含__template__的页面返回，就要将登录用户的信息带回，没登录的就是None，登陆成功的就是user对象
                r['__user__'] = request.__user__
                # logging.info('shy>>>>>>>>>>>>>>>>>>>>>>>>>' + request.__user__)
                # logging.info('shy>>>>>>>>>>>>>>>>>>>>>>>>>' + r['__user__'])
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        # 数字的response是状态码
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

# 给模板文件添加的filter，让模板自己带有一些自定义的功能函数
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


async def init(loop):
    await orm.create_pool(loop=loop, **configs.db)
    # middleware是一种拦截器，一个URL在被某个函数处理前后，可以经过一系列的middleware的处理
    # 调用过程是：url request -> middlewares -> RequestHandler -> (请求)handler(返回) -> RequestHandler -> middlewares -> url response
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, response_factory
    ])
    # 初始化jinja2模板组件，并且给模板添加filter，增加获取时间的功能
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    # 'handlers'模块里定义的都是请求的处理函数（就是controls）
    add_routes(app, 'handlers')
    # 添加静态资源：/static/下的资源
    add_static(app)

    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8888)
    logging.info('server started at http://127.0.0.1:8888...')
    return srv

    # app = web.Application(loop=loop)
    # app.router.add_route('GET', '/', index)
    # srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8888)
    # logging.info('server started at http://127.0.0.1:8888')
    # return srv

# asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()




