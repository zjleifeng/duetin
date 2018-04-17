# -*- coding: utf-8 -*-

"""
Create at 2017/3/21
录音数据模型
"""

from __future__ import unicode_literals
from django.db import models
from app_auth.models import User
from dao.models.music import AllSongMusic


# class Notification(models.Model):
#
#
#     """
#     消息模型
#     """
#     title = models.CharField(max_length=20,blank=True, null=True, verbose_name=u'标题')
#     text = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'内容')
#     link = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'链接')
#     from_user = models.ForeignKey(User, default=None, blank=True, null=True, related_name='from_user_notifaction',
#                                   verbose_name=u'发送者')
#     # action_user=models.ForeignKey(User, default=None, blank=True, null=True, related_name='action_user_notifaction',
#     #                               verbose_name=u'被执行活动的人')
#     post=models.CharField(max_length=200,blank=True,null=True,verbose_name=u'相关作品ID')
#     all_post=models.ForeignKey(AllSongMusic,blank=True,null=True,related_name='allsong_music_notifaction',verbose_name=u'相关作品')
#     to_user = models.ForeignKey(User, related_name='to_user_notifaction', verbose_name=u'接受者')
#     type = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'类型')
#     is_read = models.BooleanField(default=False, verbose_name=u'是否已读')
#     created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
#     is_delete = models.BooleanField(default=False)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#
#     class Meta:
#         verbose_name_plural = u'消息管理'
#         ordering = ('-created_at',)
#
#     def timesince(self, now=None):
#         """
#         Shortcut for the ``django.utils.timesince.timesince`` function of the
#         current timestamp.
#         """
#         from django.utils.timesince import timesince as timesince_
#         return timesince_(self.created_at, now)
#
#     def __str__(self):
#         return self.title
