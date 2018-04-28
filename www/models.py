# encoding: utf-8
"""
@version: v1.0
@author: autumner
@license: Apache Licence
@contact: 18322313385@163.com
@site: https://github.com/nzj1981/mywebapp_py36.git
@software: PyCharm
@file: models.py
@time: 2018/4/23 16:56
"""

__author__ = 'autumner'

'''
create Models for user, blog, comment.
'''

import time
import uuid

from orm import Model, StringField, BooleanField, FloatField, TextField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


# create User class
class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(32)')
    admin = BooleanField()
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)




# create Blog class
class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


# create Comment class
class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)