#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/3/29 下午12:32
@SOFTWARE:PyCharm
"""
from django.conf.urls import include, url
from views import SongBookNewView, SongBookRecommendView, BannerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'songbook-recommend', SongBookRecommendView)
router.register(r'songbook-new', SongBookNewView)
router.register(r'banner', BannerViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
]
