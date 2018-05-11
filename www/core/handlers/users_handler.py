# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: users_handler.py
@time: 2018/4/25 16:08
"""

__author__ = 'autumner'

'''
users handlers
'''


import re, json, logging, hashlib
from aiohttp import web
from coroweb import get, post
from db.models.model import User, next_id
from checks.apis import APIValueError, APIError, Page
from core.handlers.handler import user2cookie, COOKIE_NAME, get_page_index



@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')

    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')

    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')

    users = await User.findAll('email=?', [email])

    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')

    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    # image use http://www.gravatar.com
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()

    # make session cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r




@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')

    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')

    users = await User.findAll('email=?', [email])

    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')

    user = users[0]

    # check password
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')

    # authenticate ok, set cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


# 用户管理页面
@get('/manage/users')
def manage_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page),
        'title': '用户管理'
    }


# 用户管理列表JSON
@get('/api/users')
async def api_get_users(request, *, page='1'):
    page_index = get_page_index(page)
    req_user = request.__user__
    if req_user.admin == 1:
        num = await User.findNumber('count(id)')
    elif req_user.admin == 2:
        num = await User.findNumber('count(id)', where='admin in (?,?)', args=(0, 2))
    p = Page(num, page_index)
    if req_user.admin == 1:
        users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
        for u in users:
            u.passwd = '******'
    elif req_user.admin == 2:
        users = await User.findAll(where='admin in (?,?)', args=[0, 2], orderBy='created_at desc', limit=(p.offset, p.limit))
        for u in users:
            u.passwd = '******'
    return dict(page=p, users=users)