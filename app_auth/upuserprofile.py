#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: upuserprofile.py
@time: 2017/6/23 下午5:52
@SOFTWARE:PyCharm
"""


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        # profile = user.get_profile()
        if user:
            user.picture = response.get('picture')['data']['url']

            user.save()
    if backend.name == 'twitter':
        if user:
            user.picture = response.get('profile_image_url')
            user.save()

    if backend.name=='instagram':
        if user:
            user.picture=response.get('data')['profile_picture']
            user.save()