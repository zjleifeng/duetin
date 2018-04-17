#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/7/17 下午2:08
@SOFTWARE:PyCharm
"""
from django.conf.urls import url
from .views import InviteView, FollowingView, Message_count_View, About_You_View, ExceptionCaseView, Song_Exception_View,ChangeCount

urlpatterns = [
    url(r'^message-count/$', Message_count_View.as_view()),
    url(r'^invited/$', InviteView.as_view()),
    url(r'^you/$', About_You_View.as_view()),
    url(r'^myfollowing/$', FollowingView.as_view()),  # 我关注的人的动态
    url(r'^exceptioncase/$', ExceptionCaseView.as_view()),  # 异常POst
    url(r'^song-exception/$', Song_Exception_View.as_view()),  # 歌曲问题反馈
    # url(r'^changecount/$', ChangeCount.as_view()),

]