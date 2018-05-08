# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: test_file_path.py 
@time: 2018/5/8 11:51
"""

__author__ = 'autumner'

import os, sys

print(__file__)
print(os.path.abspath(__file__))
print(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'static'))
