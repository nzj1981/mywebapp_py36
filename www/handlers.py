# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: handlers.py 
@time: 2018/4/25 16:08
"""

__author__ = 'autumner'

'''
url handlers
'''


import re, time, json, logging, hashlib, base64, asyncio
import markdown2
from aiohttp import web
from coroweb import get, post
from models import User, Comment, Blog, next_id
from apis import APIValueError, APIResourceNotFoundError, APIError, APIPermissionError
from config import configs


# set cookie name
COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


# 检查用户是否是管理员
def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


# 获取页面数,作为分页使用
def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


# text to html
def text2html(text):
    lines = map(lambda s: '<p>%s<p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)






# user to cookie and set max time
def user2cookie(user, max_age):
    '''
    Generate cookie str by user
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid
    '''

    if not cookie_str:
        return None

    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None

        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None



@get('/')
async def index(request):
    blogs = await Blog.findAll()

    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }


@get('/manage/')
def manage(request):
    return {
        '__template__': 'manage.html'
    }


@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    return dict(users=users)


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


# blog to page
@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }