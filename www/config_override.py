# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: config_override.py 
@time: 2018/4/23 11:28
"""

__author__ = 'autumner'


'''
Override configurations
用于正式环境的配置文件
'''

configs = {
    'db': {
        'host': '127.0.0.1',
        'port': 8094,
        'user': 'pyuser',
        'password': 'pyuser123',
        'db': 'awesome'
    }
}

