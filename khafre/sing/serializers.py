#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: serializers.py
@time: 2017/5/11 下午6:42
@SOFTWARE:PyCharm
"""
from rest_framework import serializers
from dao.models.base import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'content', 'img', 'link')


