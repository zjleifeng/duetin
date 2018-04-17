#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: utils.py
@time: 2017/4/27 下午7:08
@SOFTWARE:PyCharm
"""
import re,datetime

PASSWORD_MAX_LENGTH = 20
PASSWORD_MIN_LENGTH = 6
PASSWORD_PATTERN = r'[0-9a-zA-Z]+'
password_regex = re.compile(PASSWORD_PATTERN)


def is_valid_password(password):
    length_of_pwd = len(password)
    if length_of_pwd < PASSWORD_MIN_LENGTH or length_of_pwd > PASSWORD_MAX_LENGTH:
        return False
    return True
    
    # return password_regex.fullmatch(password)
def is_valid_username(username):
    # username_str = ''.join(username.split())
    # if len(username)>len(username_str):
        # return "username can't connect blank"
        # return False
    if not re.search(r'^[a-zA-Z0-9_]{1,30}$', username, re.U):
        # return "username can't connect special character!"
        return False

    # if len(username_str) < 4 or len(username_str)>20:
    #     return "username can't Less than 4 characters or more than 20 characters!"
        # return False

    return True


def mylogin(request, user):
    if user is None:
        user = request.user
    this_time = datetime.datetime.now()
    user.last_login = this_time
    user.save()