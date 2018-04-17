#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: language.py
@time: 2018/4/3 下午10:21
@SOFTWARE:PyCharm
"""

from django.http import HttpResponse
from django.shortcuts import render
from khufu import settings
from khufu.settings import en_lan,id_lan
from khafre.utils.json_response import json_resp


try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class CheckVersionsMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if request.environ.has_key("HTTP_VERSION"):
            version=request.environ['HTTP_VERSION']

            if version=="1.0.36":
                pass
            else:
                pass
                # return json_resp(code=499,msg="new")
        else:
            pass
            # return json_resp(code=499, msg="new")


def check_lan(request):
    if request.META.has_key("HTTP_X_LOCALE"):
        lang = request.environ['HTTP_X_LOCALE']

        if lang == "id":
            return id_lan
        else:
            return en_lan

    else:
        return en_lan
