#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: exceptions.py
@time: 2017/8/30 下午1:19
@SOFTWARE:PyCharm
自定义错误信息格式
"""


from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = response.status_code
        response.data['msg'] = response.data['detail']
        del response.data['detail']

    return response