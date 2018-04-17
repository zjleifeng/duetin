#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/10/12 下午1:10
@SOFTWARE:PyCharm
"""
from django.conf.urls import *
from django.conf.urls import url, include
from khafre.sing.views import SingIndexView, Search_sing, SingView, SingjoinView, BannerView, Report_View, \
    post_callback, TopSortView, sing_callback
from django.views.decorators.cache import cache_page
from .views import userlogin, forgetpassword, Post_data_View, PostDataSearch_View, Del_postdata, allpostdata
from .views import operate, UsersView, UserSearchView, edituser, Music_View, MusicSearch_View, Edit_music, \
    Post_View, PostSearch_View, Edit_Post, logout, Sing_Recommend_View, Singsearch_Recommend_View, Edit_Sing_Recommend, \
    NewSing_Recommend_View, NewSingsearch_Recommend_View, Edit_NewSing_Recommend, DayPost_View, Up_Mobilejson, \
    Mobileversearch, Edit_Mobilever, MobileVersion_View, AllPost_View, CheckDb, Del_Post, Top50_recommend, \
    TopSingsearch_Recommend_View, Edit_TopSing_Recommend, Test, Newuser_recommend_View, Newuser_recommendSearch_View, \
    EditNewuser_recommend, Partscore_View, Searchpartscore_View, Editpartscore, Del_partpost, shuju, MusicOperate_View, \
    MusicOperateSearch_View, Edit_MusicNoOperate, MusicOperate_no_View, MusicOperateNoSearch_View, Category_View, \
    CategorySearch_View, Edit_Category, Category_Set_View, Edit_CategorySet, Create_Category_Set_View, Song_Case_View, \
    Song_Case_Search_View, Edit_SongCase, Del_Songcase_View,ManualPost_View,ManualPost_Search_View
from khafre.manage.views import upmusic_file, upsinger_file, conversion_toid,upmusictime_file

urlpatterns = [
    url(r'^$', operate),
    url(r'^login/$', userlogin, name="userlogin"),
    url(r'^logout/$', logout, name="logout"),

    url(r'^userrecord/$', UsersView.as_view(), name='users-view'),
    url(r'^usersearch/$', UserSearchView.as_view(), name='usersearch-view'),
    url(r'^edituser/(?P<pk>[0-9]+)/$', edituser.as_view(), name='edituserecord-view'),

    url(r'^musicrecord/$', Music_View.as_view(), name='music-view'),
    url(r'^musicsearch/$', MusicSearch_View.as_view(), name='musicsearch-view'),
    url(r'^editmusic/(?P<pk>[0-9]+)/$', Edit_music.as_view(), name='editmusicrecord-view'),

    url(r'^musicoperate/$', MusicOperate_View.as_view(), name='musicoperate-view'),
    url(r'^musicnooperate/$', MusicOperate_no_View.as_view(), name='musicoperateno-view'),
    url(r'^musicoperatesearch/$', MusicOperateSearch_View.as_view(), name='musicoperatesearch-view'),
    url(r'^musicoperatenosearch/$', MusicOperateNoSearch_View.as_view(), name='musicoperatenosearch-view'),
    url(r'^editmusinocoperate/(?P<pk>[0-9]+)/$', Edit_MusicNoOperate.as_view(), name='editmusicnooperate-view'),

    url(r'^postrecord/$', Post_View.as_view(), name='post-view'),
    url(r'^daypostrecord/$', DayPost_View.as_view(), name='daypost-view'),
    url(r'^allpostrecord/$', AllPost_View.as_view(), name='allpost-view'),

    url(r'^postsearch/$', PostSearch_View.as_view(), name='postsearch-view'),
    url(r'^editpost/(?P<pk>[0-9]+)/$', Edit_Post.as_view(), name='editpostrecord-view'),
    url(r'^delpost/(?P<pk>[0-9]+)/$', Del_Post.as_view(), name='delpostrecord-view'),

    url(r'^create_category_set/$', Create_Category_Set_View.as_view(), name='create_category_set-view'),
    url(r'^category_set/$', Category_Set_View.as_view(), name='category_set-view'),
    url(r'^editcategory_set/(?P<pk>[0-9]+)/$', Edit_CategorySet.as_view(), name='editcategory_set-view'),
    url(r'^category/$', Category_View.as_view(), name='category-view'),
    url(r'^categorysearch/$', CategorySearch_View.as_view(), name='categorysearch-view'),
    url(r'^editcategory/(?P<pk>[0-9]+)/$', Edit_Category.as_view(), name='editcategory-view'),

    url(r'^sing-recommend/$', Sing_Recommend_View.as_view(), name='sing-recommend-view'),
    url(r'^singsearch-recommend/$', Singsearch_Recommend_View.as_view(), name='singsearch-recommend-view'),
    url(r'^editsing-recommend/(?P<pk>[0-9]+)/$', Edit_Sing_Recommend.as_view(), name='editsing-recommend-view'),

    url(r'^top50-recommend/$', Top50_recommend.as_view(), name='top-recommend-view'),
    url(r'^topsingsearch-recommend/$', TopSingsearch_Recommend_View.as_view(), name='topsingsearch-recommend-view'),
    url(r'^edittopsing-recommend/(?P<pk>[0-9]+)/$', Edit_TopSing_Recommend.as_view(),
        name='edittopsing-recommend-view'),

    url(r'^newuser-recommend/$', Newuser_recommend_View.as_view(), name='newuser-recommend-view'),
    url(r'^newusersearch-recommend/$', Newuser_recommendSearch_View.as_view(), name='newusersearch-recommend-view'),
    url(r'^editnewuser-recommend/(?P<pk>[0-9]+)/$', EditNewuser_recommend.as_view(), name='editnewuser-recommend-view'),

    url(r'^newsing-recommend/$', NewSing_Recommend_View.as_view(), name='newsing-recommend-view'),
    url(r'^newsingsearch-recommend/$', NewSingsearch_Recommend_View.as_view(), name='newsingsearch-recommend-view'),
    url(r'^editnewsing-recommend/(?P<pk>[0-9]+)/$', Edit_NewSing_Recommend.as_view(),
        name='editnewsing-recommend-view'),

    url(r'^up-mobilejson/$', Up_Mobilejson, name='upmobilejson-view'),  # 导入singer EXCEL数据

    url(r'^mobilever/$', MobileVersion_View.as_view(), name='mobilever-view'),
    url(r'^mobileversearch/$', Mobileversearch.as_view(), name='search-mobilever-view'),
    url(r'^editmobilever/(?P<pk>[0-9]+)/$', Edit_Mobilever.as_view(), name='editmobilever-view'),

    url(r'^partscore/$', Partscore_View.as_view(), name='partscore-view'),
    url(r'^searchpartscore/$', Searchpartscore_View.as_view(), name='searchpartscore-view'),
    url(r'^editpartscore/(?P<pk>[0-9]+)/$', Editpartscore.as_view(), name='editpartscore-view'),
    url(r'^delpartpost/(?P<pk>[0-9]+)/$', Del_partpost.as_view(), name='delpartpost-view'),

    url(r'^up-singer/$', upsinger_file, name='upsinger-view'),  # 导入singer EXCEL数据
    url(r'^up-music/$', upmusic_file, name='upmusic-view'),  # 导入singer EXCEL数据
    url(r'^conversion/$', conversion_toid, name='conversion-view'),  # 导入singer EXCEL数据
    url(r'^up-musictime/$', upmusictime_file, name='upmusictime-view'),  # 导入misic time EXCEL数据



    url(r'^song_case/$', Song_Case_View.as_view(), name='song-case-view'),
    url(r'^songcasesearch/$', Song_Case_Search_View.as_view(), name='songcasesearch-view'),
    url(r'^editsongcase/(?P<pk>[0-9]+)/$', Edit_SongCase.as_view(), name='editsongcase-view'),
    url(r'^delsongcase/(?P<pk>[0-9]+)/$', Del_Songcase_View.as_view(), name='delsongcase-view'),
    #  url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
    #      {'next_page': '/accounts/login/'}, name="userlogout"),
    #  url(r'^accounts/changepwd/$', 'assets.views.changepwd',name='changepwd'),
    #
    url(r'^forgetpassword/$', forgetpassword, name='forgetpassword-view'),
    url(r'^manualpost/$', ManualPost_View.as_view(), name='manualpost-view'),
    url(r'^manualpostsearch/$', ManualPost_Search_View.as_view(), name='manualpostsearch-view'),

    url(r'^checkdb/$', CheckDb.as_view()),
    url(r'^test/$', shuju),
    # url(r'^postdata/$', Post_data_View.as_view()),
    # url(r'^postdatasearch/$', PostDataSearch_View.as_view(), name='searchpostdata-view'),
    # url(r'^delpostdata/(?P<pk>[0-9]+)/$', Del_postdata.as_view(), name='delpostdata-view'),
    url(r'^allpostdata/$', allpostdata.as_view()),

]
