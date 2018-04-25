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

from coroweb import get, post
from models import User, Comment, Blog, next_id


@get('/')
async def index(request):
    users = await User.findAll()
    blogs = await Blog.find('0015246275670282790f1d86ce04c768501391fd6f1acc7000')
    u = await User.findNumber('id', 'name = ?', 'Test2')
    print(u)
    return {
        '__template__': 'index.html',
        'users': users,
        'blogs': blogs
    }