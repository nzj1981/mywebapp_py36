# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: test_table_user.py 
@time: 2018/4/23 17:06
"""

__author__ = 'autumner'


'''
output user password
'''

import asyncio
from db import orm
from conf.config import configs
from db.models.model import User
import hmac
import hashlib

# 给密码加密
def hmac_md5(key, s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()

email = 'zhangsang@163.com'
# set password
passwd = '123456'
passwd1 = ('%s:%s' % (email, passwd)).encode('utf-8')
loop = asyncio.get_event_loop()
loop.run_until_complete(orm.create_pool(loop=loop, **configs.db))
rs = loop.run_until_complete(User.findAll('email=?', [email]))
user = dict(rs[0])
passwd1= hashlib.sha1(passwd1).hexdigest()
sha1_passwd = ('%s:%s' % (user['id'], passwd1)).encode('utf-8')
sha1_passwd = hashlib.sha1(sha1_passwd).hexdigest()
print(sha1_passwd)
loop.run_until_complete(orm.close_pool())
# loop.run_forever()