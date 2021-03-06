# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: app.py 
@time: 2018/4/20 13:36
"""

__author__ = 'autumner'

'''
Web App基本服务搭建
'''

import logging;

logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time

from datetime import datetime

from aiohttp import web


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), 'localhost', 9000)
    logging.info('Server started at http://%s:%s...' % ('localhost', '9000'))
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
