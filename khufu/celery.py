#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: celery.py.py
@time: 2017/6/1 下午1:29
@SOFTWARE:PyCharm
"""

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
# from khufu import settings
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khufu.settings')

app = Celery('khafre')
# appauth=Celery('app_auth')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# appauth.config_from_object('django.conf:settings')
# appauth.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
