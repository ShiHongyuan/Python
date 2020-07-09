#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shihongyuan'



'''
请求的处理函数（就是controls或者servers），在web框架里，增加一个业务只需要在这里添加对应的处理函数就行了
'''

import re, time, json, logging, hashlib, base64, asyncio
from aiohttp import web

import markdown2
from models import User, Comment, Blog, next_id
from coreweb import get, post
from apis import Page, APIError, APIValueError, APIResourceNotFoundError, APIPermissionError
from config import configs


@get('/blog/example')
def get_blogs_example(request):
    '''
    获取日志页面示例
    '''
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]

    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }


@get('/api/users/example')
async def api_get_users_example(*, page='1'):  ###### *后面是命名关键字参数
    '''
    restful请求风格的api示例
    '''
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    # 只要返回一个dict，后续的response这个middleware就可以把结果序列化为JSON并返回
    return dict(users=users)





# 创建cookie相关
COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_signin(request):
    '''
    通过验证request有没有绑定用户，判断用户有没有登陆且登陆的cookie是否有效
    :param request:
    :return:
    '''
    if request.__user__.id is None:
        raise APIPermissionError('请先登录，或cookie无效请重新登录.')
def check_admin(request):
    '''
    通过验证request有没有绑定用户，且用户是不是管理员，判断用户能否创建/编辑blog的权限
    '''
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError('您未登陆或您不是管理员')


def get_page_index(page_str):
    '''
    读取页数由str转换为int，如果有误，返回1
    '''
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def text2html(text):
    '''
    从数据库里读出的str数据，可能包含html的保留字符，将这些字符转换成转换成html能识别的字符实体，返回html能展示的文本数据
    :param text:
    :return:
    '''
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


@get('/')
async def index(request):
    '''
    请求首页示例
    '''
    # 必须加await，等协程执行完毕，再执行下面的，否则在没有执行完的情况下users是一个协程对象，获取不了值
    users = await User.findAll()
    # 返回是一个list
    logging.info(users)
    # 返回首页的模板
    return {
        '__template__': 'test.html',
        'users': users
    }


'''
用户注册和登录功能
'''
# 编译正则
_RE_EMAIL = re.compile(r'^[a-zA-Z0-9\.\-\_]+\@[a-zA-Z0-9\-\_]+(\.[a-zA-Z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


def user2cookie(user, max_age):
    '''
    依赖user的属性生成cookie str
    '''
    # build cookie string by: id-expires-sha1
    # 超时的时间
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    # cookie的组成有三部分：userid + 过期时间 + 加密后的数字签名
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


# 这个很神奇，如果用async标注协程的话，在if里面的return会不允许，所以只能用@asyncio.coroutine和yield from了
@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    验证用户的cookie是否有效
    :return: 有效返回user，无效返回None
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        logging.info('shy++++++++++++++++++++++++' + str(len(L)))
        if len(L) != 3:
            return None
        # 取出cookie的三部分
        uid, expires, sha1 = L
        logging.info('shy++++++++++++++++++++++++' + uid)
        logging.info('shy++++++++++++++++++++++++' + expires)
        logging.info('shy++++++++++++++++++++++++' + sha1)
        if int(expires) < time.time():
            logging.info('shy++++++++++++++++++++++++' + str(time.time()))
            return None
        # 重新加密验证数字签名
        user = yield from User.findById(uid)
        s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        logging.info('shy*************************' + user.id)
        return user
    except Exception as e:
        logging.exception(e)
        return None


@post('/api/register')
async def api_register_user(*, email, name, passwd):
    '''
    用户注册
    :return: 注册成功返回保存的user信息，注册失败返回api的错误
    '''
    if not name or not name.strip():
        raise APIValueError('name', message='名字为空')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email', message='邮箱有误')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd', message='密码有误')
    # 用户判重的原则是邮箱相同，所以查找时传入where的搜索关键字email
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('注册失败', 'email', '邮箱已经被注册!')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    # 保存用户信息2DB
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    # json.dumps()用于将字典形式的数据序列化为字符串
    # json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@post('/api/authenticate')
async def authenticate(*, email, passwd):
    '''
    用户登录
    :param email: 用邮箱当账户名登录
    :param passwd:
    :return: 验证成功返回user信息，验证失败返回api的错误
    '''
    if not email:
        raise APIValueError('email', '邮箱无效.')
    if not passwd:
        raise APIValueError('passwd', '密码无效')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', '邮箱不存在.')
    user = users[0]
    # check passwd:
    # 生成密码的原始数据是：'%s:%s' % (uid, passwd)
    sha1_passwd = '%s:%s' % (user.id, passwd)
    sha1 = hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()

    # sha1 = hashlib.sha1()
    # sha1.update(user.id.encode('utf-8'))
    # sha1.update(b':')
    # sha1.update(passwd.encode('utf-8'))

    if user.passwd != sha1:
        raise APIValueError('passwd', '密码错误.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/register')
def register(request):
    '''
    返回注册页面
    :return:
    '''
    return {
        '__template__': 'register.html',
        # 注册成功，跳转之前的页面，后端做了处理，如果之前页面有误，就跳转首页
        'referer': request.headers.get('Referer') or '/'
    }


@get('/signin')
def signin(request):
    '''
    返回登录页面
    :param request:
    :return:
    '''
    return {
        '__template__': 'signin.html',
        # 登录成功，跳转之前的页面，后端做了处理，如果之前页面有误，就跳转首页
        'referer': request.headers.get('Referer') or '/'
    }


@get('/signout')
def signout(request):
    '''
    注销登录的请求
    :param request:
    :return:
    '''
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    # 退出账号，删除cookie，跳转到请求注销时所在的页面
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r



'''
comments页面相关
'''

@get('/manage/')
def manage():
    '''
    重定向到comments的列表页面
    :return:
    '''
    return 'redirect:/manage/comments'

@get('/manage/comments')
# 第一次请求的时候，是不带有page参数的，page就取默认值1
def manage_comments(*, page='1'):
    '''
    返回comments的列表页面
    :param page:
    :return:
    '''
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
    }

@get('/api/comments')
async def api_comments(*, page='1'):
    '''
    获取comments列表的数据（api）
    :param page:
    :return:
    '''
    page_index = get_page_index(page)
    num = await Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)


@post('/api/comments/{id}/delete')
async def api_delete_comments(id, request):
    '''
    管理员在评论列表页删除评论
    :param id:
    :param request:
    :return:
    '''
    check_admin(request)
    c = await Comment.findById(id)
    if c is None:
        raise APIResourceNotFoundError('Comment', '该条评论未找到，删除失败')
    await c.remove()
    return dict(id=id)





'''
blog页面相关
'''

'''
blog列表页
'''
@get('/manage/blogs')
def manage_blogs(*, page='1'):
    '''
    blog的列表页面
    :param page:
    :return:
    '''
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


@get('/api/blogs')
async def api_blogs(*, page='1'):
    '''
    blog列表的数据（api）
    :param page:
    :return:
    '''
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


'''
blog详情页
'''

@get('/blogs/{id}')
async def get_blog(id):
    '''
    返回某一个blog详情的页面
    :param id:
    :return:
    '''
    blog = await Blog.findById(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        # 将一些html的特殊字符转换成html可以识别的字符实体
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments,
    }


@post('/api/blogs/{id}/comments/create')
async def api_create_comment(id, request, *, content):
    '''
    在blog详情页创建评论保存（api）
    :param id:
    :param request:
    :param content:
    :return:
    '''
    # 已登录用户才有权限评论blog
    check_signin(request)
    user = request.__user__
    if not content or not content.strip():
        raise APIValueError('content', '请输入评论内容！')
    blog = await Blog.findById(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog', '评论此博客出错！')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    await comment.save()
    return comment


@get('/manage/blogs/create')
def manage_create_blog():
    '''
    返回创建新的blog的页面
    :return:
    '''
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs/create'
    }


@post('/api/blogs/create')
# *后面是命名关键字参数
async def api_create_blog(request, *, name, summary, content):
    '''
    创建保存新的blog
    :param request:
    :param name:
    :param summary:
    :param content:
    :return:
    '''
    # 只有创建新的blog，才需要验证已经登录的cookie，并且是管理员admin身份才有权新建
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', '请输入日志标题.')
    if not summary or not summary.strip():
        raise APIValueError('summary', '请输入日志摘要.')
    if not content or not content.strip():
        raise APIValueError('content', '请输入日志内容.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    '''
    通过blog的id返回相应blog的编辑页面
    :param id:
    :return:
    '''
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s/update' % id
    }

@get('/api/blogs/{id}')
async def api_get_blog(id):
    '''
    编辑一个blog的时候，返回需要代入编辑页面的数据（api）
    :param id:
    :return:
    '''
    blog = await Blog.findById(id)
    return blog


@post('/api/blogs/{id}/update')
async def api_update_blog(id, request, *, name, summary, content):
    '''
    保存编辑更新的blog（api）
    :param id:
    :param request:
    :param name:
    :param summary:
    :param content:
    :return:
    '''
    # 只有已登录的管理员admin才有权限编辑更新blog
    check_admin(request)
    blog = await Blog.findById(id)
    if not name or not name.strip():
        raise APIValueError('name', '请输入日志标题.')
    if not summary or not summary.strip():
        raise APIValueError('summary', '请输入日志摘要.')
    if not content or not content.strip():
        raise APIValueError('content', '请输入日志内容.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog


@post('/api/blogs/{id}/delete')
async def api_delete_blog(request, *, id):
    '''
    根据id删除某一个blog
    :param request:
    :param id:
    :return:
    '''
    # 只有已登录的管理员admin才有权限删除blog
    check_admin(request)
    blog = await Blog.findById(id)
    await blog.remove()
    return dict(id=id)





'''
users页面相关
'''

@get('/manage/users')
def manage_users(*, page='1'):
    '''
    返回所有注册用户的列表页面
    :param page:
    :return:
    '''
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }



@get('/api/users')
async def api_get_users(*, page='1'):
    '''
    获取所有注册用户的数据（api）
    '''
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    # 只要返回一个dict，后续的response这个middleware就可以把结果序列化为JSON并返回
    return dict(page=p, users=users)

















