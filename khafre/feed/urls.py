#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/5/22 下午5:33
@SOFTWARE:PyCharm
"""
from django.conf.urls import url, include
from .views import Feed,Music_Click_Count_View

urlpatterns = [
    url(r'^$',Feed.as_view()),
    url(r'^clickcount/$', Music_Click_Count_View.as_view()),

]