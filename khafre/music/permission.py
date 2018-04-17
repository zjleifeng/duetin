#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: permission.py
@time: 2017/4/10 下午12:40
@SOFTWARE:PyCharm
"""
from rest_framework import permissions


class IsAdminCreateOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser
