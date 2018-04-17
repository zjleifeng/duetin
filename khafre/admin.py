#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: admin.py
@time: 2017/4/28 上午11:33
@SOFTWARE:PyCharm
"""
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from django.contrib import admin
from dao.models.music import AllSongMusic, PartSongMusic, MusicProfiel, Singer, PartComment, ALLComment, Notification, \
    AboutyouNotification, AllMusicCategory
from dao.models.base import Banner


class SingerAdmin(admin.ModelAdmin):
    search_fields = ('singer_name', 'uid')
    list_filter = ('singer_name', 'uid')
    list_display = ('singer_name', 'uid')
    # fields = ('__all__',)


class MusicAdmin(admin.ModelAdmin):
    search_fields = ('music_name', 'uid')
    list_filter = ('music_name', 'uid')
    list_display = (
    'music_name', 'uid', 'bucket_original_key', 'bucket_accompany_key', 'accompany', 'lyrics', 'bucket_lyrics_key',
    'image', 'bucket_image_key', 'is_loved', 'is_online')


class ALLsongMusicAdmin(admin.ModelAdmin):
    search_fields = ('id', 'music_info__music_name', 'all_music_auth__username')
    # list_filter = ('music_info',)
    list_display = ('id', 'music_info', 'title', 'music_auth_part', 'music_participant_part', 'all_music_auth',
                    'vedio', 'view_count', 'is_delete', 'rank', 'is_enable')


class PartSongMusicAdmin(admin.ModelAdmin):
    search_fields = ('id', 'music_info__music_name', 'music_auth__username')

    list_display = ('id', 'music_info', 'title', 'part', 'created_at', 'is_enable', 'is_delete')


class AllCommentAdmin(admin.ModelAdmin):
    search_fields = ('id', 'owner__username')
    list_display = ('id', 'music', 'owner', 'text')


admin.site.register(Singer, SingerAdmin)
admin.site.register(MusicProfiel, MusicAdmin)
admin.site.register(PartSongMusic, PartSongMusicAdmin)
admin.site.register(PartComment)
admin.site.register(AllSongMusic, ALLsongMusicAdmin)
admin.site.register(ALLComment, AllCommentAdmin)
admin.site.register(Banner)
admin.site.register(Notification)
admin.site.register(AboutyouNotification)
admin.site.register(AllMusicCategory)
