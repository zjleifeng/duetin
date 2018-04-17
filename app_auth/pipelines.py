#!/usr/bin/env python
# encoding: utf-8

from app_auth.models import User
# 這個 pipeline 只有在處理 Oauth Account 的時候會用到
def save_profile(backend, *args, **kwargs):
    
    username = kwargs.get('username')
    details = kwargs.get('details')
    email = details.get('email')
    fullname = details.get('fullname')

    # clean email to disable find password
    user = User.objects.get(username=username)
    
    # init user profile
    if user.nickname=="":
        user.nickname=fullname
    if user.email=="":
        user.email=email
    user.save()


