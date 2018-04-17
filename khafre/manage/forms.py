#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: forms.py
@time: 2017/6/19 下午2:41
@SOFTWARE:PyCharm
"""
from django import forms


class UpForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()
    # upform = forms.FileField(required=True, error_messages={
    #     'required': u'必须选择一个导入文件',
    #     'invalid': u'上传文件是以xls结尾的excel'})