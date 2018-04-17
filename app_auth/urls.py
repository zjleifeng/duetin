#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/4/27 下午7:06
@SOFTWARE:PyCharm
"""

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    GeneralSignUpView,
    ProfileView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    FindPasswordView,
    ResetPasswordView,
    FollowersView,
    FollowingView,
    FollowView,
    ProfileUserView,
    RegisterEmailView,
    SuggestView,
    Social_login_View,
    register_by_token,
    Newuser_Edit_View,
    InviteFolloeView,
    SearchUserView,
    Get_STStokenView,
    SendMSG,
    Get_IP,
    FcmTokenView,
    Mobile_Version_view,
    User_List_View,
    User_Recommend_View,
    NewUser_FollowView,First_Edit_Pro_View,First_User_Info_View,testutc,
    Reg_Ins,Get_Token_Byins,Ins_Photo,User_Ins_Photo,Binding_Ins_View,Release_Ins_View,Ali_Oss_Auth_View
)
from khufu.views import obtain_expiring_auth_token

urlpatterns = [

    url(r'^register/$', GeneralSignUpView.as_view()),
    url(r'^fcmtoken/$', FcmTokenView.as_view()),
    url(r'^mobile-version/$', Mobile_Version_view.as_view()),  # 更新手机信息

    # url(r'^token/', obtain_expiring_auth_token, name='api-token'),  # 用username，password获取token##暂时不用
    # url(r'^sociallogin/', Social_login_View.as_view()),  # 第三方登录回传地址#暂时废弃使用
    url(r'^login/$', LoginView.as_view()),  # 用户名或者邮箱，密码登录，返回用户信息以及yoken，暂时不用
    url(r'^logout/$', LogoutView.as_view()),  # APP端不需要用
    url(r'^profile/$', ProfileView.as_view()),  # 登录用户个人信息
    url(r'^first_edit_pro/$', First_Edit_Pro_View.as_view()),
    url(r'^first_user_info/$', First_User_Info_View.as_view()),  #

    url(r'^profile/users/(?P<pk>\d+)/$', ProfileUserView.as_view()),  # 查看某用户信息
    url(r'^profile/followers/(?P<pk>\d+)/$', FollowersView.as_view()),  # 查看某人的粉丝
    url(r'^profile/following/(?P<pk>\d+)/$', FollowingView.as_view()),  # 查看某人关注的人
    url(r'^profile/invitefollow/$', InviteFolloeView.as_view()),  # 查看用户关注的人和关注他的人
    url(r'^profile/search-user/$', SearchUserView.as_view()),  # 按照用户名查询用户
    url(r'^profile/follower_edit/(?P<pk>\d+)/$', FollowView.as_view()),  # 添加、删除好友
    url(r'^profile/newuser_follower/$', NewUser_FollowView.as_view()),  # 新用户推荐添加好友
    url(r'^user_list/$', User_List_View.as_view()),  # 用户点击添加好友，显示的可添加好友列表
    url(r'^user_recommend/$', User_Recommend_View.as_view()),
    url(r'^change_password/$', ChangePasswordView.as_view()),
    url(r'^suggest/$', SuggestView.as_view()),  # 添加建议
    url(r'^find_password/$', FindPasswordView.as_view()),
    url(r'^register_email/(?P<url_token>[0-9a-f]{64})/(?P<entry_token>[0-9a-f]{6})/$', RegisterEmailView.as_view()),
    url(r'^reset_password/(?P<url_token>[0-9a-f]{64})/$', ResetPasswordView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^testsendmsg/$', SendMSG.as_view()),
    url(r'^register-by-token/$', register_by_token.as_view()),  # 第三方登录通过ACCESS-token
    url(r'^new-user-edit/$', Newuser_Edit_View.as_view()),
    url(r'^get-ststoken/$', Get_STStokenView.as_view()),
    url(r'^getipadress/$', Get_IP.as_view()),
    url(r'^reg_ins/$', Reg_Ins.as_view()),
    url(r'^get_token_ins/$',Get_Token_Byins.as_view()),
    url(r'^ins_photo/$', Ins_Photo.as_view()),
    url(r'^user_ins_photo/(?P<pk>\d+)/$', User_Ins_Photo.as_view()),  # 查看某用户信息

    url(r'^binding_ins/$', Binding_Ins_View.as_view()),
    url(r'^release_ins/$', Release_Ins_View.as_view()),
    url(r'^ali_oss_auth/$', Ali_Oss_Auth_View.as_view()),
    # url(r'^testutc/$', testutc.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
