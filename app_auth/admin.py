#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: admin.py
@time: 2017/4/25 下午7:14
@SOFTWARE:PyCharm
"""

from django.contrib import admin
from app_auth.models import User, Fans


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'id')
    list_filter = ('username',)
    list_display = ('username', 'id', 'nickname',
                    'email', 'date_joined')


admin.site.register(User, UserAdmin)
admin.site.register(Fans)
