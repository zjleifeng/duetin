#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/3/30 下午5:06
@SOFTWARE:PyCharm
"""
from django.conf.urls import url, include
from khafre.sing.views import SingIndexView, Search_sing, SingView, SingjoinView, BannerView, Report_View, \
    post_callback, TopSortView, sing_callback,Handle_Callback,Sing_Random_View,Up_Trim_View,Search_Index_View,Search_User_View
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^banner/$', cache_page(60 * 3)(BannerView.as_view())),  # banner  GET获取BANNER数据按手动rank值排序
    url(r'^sing_index/(?P<slug>\w+)/$', SingIndexView.as_view()),  # 唱歌页面主页 GET参数slug（new，pop）
    # url(r'^sing_index/(?P<slug>\w+)/$', cache_page(60 * 1)(SingIndexView.as_view())),  # 唱歌页面主页 GET参数slug（new，pop）
    url(r'^top50/$', TopSortView.as_view()),
    url(r'^search_sing/$', Search_sing.as_view()),  # 唱歌页面搜索歌曲 post（搜索关键词"word"）
    url(
        r'^sing_song/(?P<pk1>[0-9]+)/$|^sing_song/(?P<pk2>[0-9]+)/(?P<devicename>[a-zA-Z0-9+=]+)/(?P<model>[a-zA-Z0-9+=]+)/(?P<manufacturer>[a-zA-Z0-9+=]+)/(?P<os>[a-zA-Z0-9+=]+)/$',
        SingView.as_view()),
    url(
        r'^sing_join/(?P<pk1>[0-9]+)/(?P<choice1>[0-1])/$|^sing_join/(?P<pk2>[0-9]+)/(?P<choice2>[0-1])/(?P<devicename>[a-zA-Z0-9+=]+)/(?P<model>[a-zA-Z0-9+=]+)/(?P<manufacturer>[a-zA-Z0-9+=]+)/(?P<os>[a-zA-Z0-9+=]+)/$',
        SingjoinView.as_view()),
    url(r'^search_index/$',Search_Index_View.as_view()),    #滑动匹配右侧搜索歌曲页面
    url(r'^search_user/$', Search_User_View.as_view()),     #滑动匹配右侧搜索页面根据年龄和性别搜索
    url(r'^sing_random/$', Sing_Random_View.as_view()),

    url(r'^report_song/(?P<pk>[0-9]+)/$', Report_View.as_view()),  # 歌曲举报
    url(r'^post_callback/$', post_callback.as_view()),
    url(r'^sing_callback/$', sing_callback.as_view()),  # 服务器处理时候后回掉
    url(r'^handle_callback/$', Handle_Callback.as_view()),  # 服务器处理时候后回掉
    url(r'^up_trim/$', Up_Trim_View.as_view()),  # 测试延迟后存储到数据库

]
