#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/3/29 下午12:35
@SOFTWARE:PyCharm
"""
from django.conf.urls import url
from views import PopularView, AllMusicDetail, \
    SearchSingerSongView, Del_Music_View, My_Post_View, Whos_Post_View, Music_comment_View, Musci_praise_View, \
    SearchPostView, H5shareMusic,H5shareMusict,Recommend_Vedio_View,All_Category_View


urlpatterns = [

    url(r'^allmusic_share_j/(?P<pk>[0-9]+)/$', H5shareMusic.as_view()),  # 分享html页面json数据接口
    url(r'^allmusic_share/(?P<pk>[0-9]+)/$', H5shareMusict),
    # url(r'^popular/$', cache_page(CACHE_MIDDLEWARE_SECONDS)(PopularView.as_view())),  # 主页面1
    url(r'^popular/$', PopularView.as_view()),  # 主页面
    url(r'^my_post/$', My_Post_View.as_view()),  # 用户自己所发布的视频
    url(r'^whos_post/(?P<pk>[0-9]+)/$', Whos_Post_View.as_view()),  # 查看别人发布的视频
    url(r'^all_music_detail/(?P<pk>[0-9]+)/$', AllMusicDetail.as_view()),#查看单个视频
    url(r'^praise/(?P<pk>[0-9]+)/$', Musci_praise_View.as_view()),#对视频点赞
    url(r'^music_comment/(?P<pk>[0-9]+)/$', Music_comment_View.as_view()),  # 某视频所有的评论
    url(r'^del_music/(?P<pk>[0-9]+)/$', Del_Music_View.as_view()),  # 删除自己的视频
    url(r'^search/$', SearchSingerSongView.as_view()),  # 搜索用户发布的视频/用户       POST 参数slug(people,sing)，搜索关键字word
    url(r'^search_post/(?P<pk>[0-9]+)/(?P<slug>\w+)/$', SearchPostView.as_view()),
    # 搜索用户发布的视频/用户       POST 参数slug(people,sing)，搜索关键字word
    url(r'^recommend_video/$', Recommend_Vedio_View.as_view()),#推荐给新用户的视频
    url(r'^all_category/$', All_Category_View.as_view()),#搜索下面的分类显示
]