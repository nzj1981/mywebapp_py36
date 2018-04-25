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
test table user
'''

import orm, asyncio
from config import configs
from models import User


# print(configs.get('db'), type(configs.get('db')))


u = User(name='Test2', email='test2@126.com', passwd='123456', image='about:blank')
u2 = User(id='001524538558302fbd63b3e20a74dcea9859ca7cf03481e000', name='Test2', email='test1@126.com', passwd='abcd132', image='about:blank', admin=0, created_at=1524538558.3028)

loop = asyncio.get_event_loop()
loop.run_until_complete(orm.create_pool(loop=loop, **configs.db))
rs = loop.run_until_complete(u.save())
# rs = loop.run_until_complete(u2.update())
print(rs)
rs1 = loop.run_until_complete(orm.select('select * from users', None))
print("list: %s" % rs1)
loop.run_until_complete(orm.close_pool())
loop.run_forever()