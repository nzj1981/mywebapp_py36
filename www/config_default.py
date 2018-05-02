# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: config_default.py 
@time: 2018/4/23 11:22
"""

__author__ = 'autumner'


'''
Default configurations
应用开发环境的配置文件
'''

configs = {
    'debug': True,
    'db': {
        'host': '*****',
        'port': 8094,
        'user': 'pyuser',
        'password': 'pyuser123',
        'db': 'awesome'
    },
    'session': {
        'secret': 'AweSoMe'
    },
    'server': {
        'host': 'localhost',
        'port': 9000
    }
}
