#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: myjson.py
@time: 2017/6/14 下午3:08
@SOFTWARE:PyCharm
"""

import json
from datetime import datetime
from time import mktime


###序列化celery数据，datatime为json

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': '__datetime__',
                'epoch': int(mktime(obj.timetuple()))
            }
        else:
            return json.JSONEncoder.default(self, obj)

def my_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == '__datetime__':
            return datetime.fromtimestamp(obj['epoch'])
    return obj

# Encoder function
def my_dumps(obj):
    return json.dumps(obj, cls=MyEncoder)

# Decoder function
def my_loads(obj):
    return json.loads(obj, object_hook=my_decoder)
