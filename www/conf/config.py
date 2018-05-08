# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: config.py 
@time: 2018/4/23 11:30
"""

__author__ = 'autumner'

'''
Configuration
全局配置文件
'''

class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


# override merge defaults
def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


# to dict
def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v

    return D


try:
    from conf import config_default
    configs = config_default.configs
except ImportError:
    pass

try:
    from conf import config_override, config_default

    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)

# print(type(configs.db),configs.db['host'])