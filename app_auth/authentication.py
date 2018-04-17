#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: authentication.py
@time: 2017/4/27 下午8:21
@SOFTWARE:PyCharm
"""
from app_auth.models import User

class EmailAuthBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
