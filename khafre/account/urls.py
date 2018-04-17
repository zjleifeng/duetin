#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: urls.py
@time: 2017/3/29 下午3:34
@SOFTWARE:PyCharm
"""

from django.conf.urls import url, include
from rest_framework import routers
from khafre.account import views
from rest_framework import routers
from rest_framework.authtoken import views as rest_views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

# router = routers.DefaultRouter()
# router.register(r'userslist', views.ProfileViewSet)


urlpatterns = [
    # url(r'^updept/$', 'assets.upxlwt.deptup', name='updept-view'),  # 导入EXCEL数据
    # url(r'^', include(router.urls)),
    # url(r'^login/', rest_views.obtain_auth_token),
    # url(r'^signup/?', views.post_sign_up),

    # url(r'^me/$', views.user_list),
    # url(r'^register/$', views.UserControl),
    # url(r'^editprofile/(?P<pk>\d+)$', ),
    # url(r'^auth/',include('rest_framework_social_oauth2.urls')),
    # url(r'^usercontrol/(?P<slug>\w+)$', views.UserControl.as_view(), name='usercontrol-view'),
    # url(r'^settings/(?P<slug>\w+)$', views.settings.as_view(), name='settings-view'),
    # url(r'^api/v1/user/userlist\d+/$',views.Users,name='user'),
    # url(r'^api/v1/user/block/\d+/$',views.Users,name='user'),
    # url(r'^api/v1/user/recording/\d+/$',views.UserRecording,name='user'),
]
