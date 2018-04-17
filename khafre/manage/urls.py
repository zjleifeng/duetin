#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/6/19 下午12:47
@SOFTWARE:PyCharm
"""

from django.conf.urls import url, include
from rest_framework import routers
from khafre.account import views
from rest_framework import routers
from rest_framework.authtoken import views as rest_views
from .views import upsinger_file,upmusic_file,conversion_toid,file_down

urlpatterns = [
    # url(r'^up-singer/$',upsinger_file, name='upsinger-view'),  # 导入singer EXCEL数据
    # url(r'^up-music/$', upmusic_file, name='upmusic-view'),  # 导入singer EXCEL数据
    # url(r'^conversion/$', conversion_toid, name='conversion-view'),  # 导入singer EXCEL数据
    url(r'^download/$', file_down),

]