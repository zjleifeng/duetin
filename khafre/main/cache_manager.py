#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: cache_manager.py
@time: 2017/6/1 下午7:05
@SOFTWARE:PyCharm
"""
from dao.models.music import AllSongMusic
from django_redis import get_redis_connection
from django.core.cache import cache,caches
import json
from khufu.settings import RETUN_COUNT, CACHE_MIDDLEWARE_SECONDS

RUNNING_TIMER = False

oth_db=caches['oth']
cache_count=caches["count"]
cache_hour=caches['hour_count']
cache_def=caches['default']


def read_from_cache(data_id, omg):
    """视频播放页面缓存"""

    key = 'cache_id_of_' + omg + '_' + str(data_id)
    value = cache_def.get(key)
    if value == None:
        data = None
    else:
        data = json.loads(value)
    return data


def write_to_cache(data_id, omg, data):
    key = 'cache_id_of_' + omg + '_' + str(data_id)
    cache.set(key, json.dumps(data), CACHE_MIDDLEWARE_SECONDS)


def up_notifactions_count(pk):
    """新的消息加一"""

    k="notification_count_{0}".format(pk)
    if oth_db.get(k):
        oth_db.incr(k)
    else:
        oth_db.set(k, 1, timeout=None)


def get_notifactions_count(pk):
    """获取消息数"""
    k="notification_count_{0}".format(pk)
    if oth_db.get(k):
        return oth_db.get(k)
    else:
        return 0


def del_notifactions_count(pk):
    """清空消息数"""
    k="notification_count_{0}".format(pk)
    oth_db.set(k, 0, timeout=None)


def notifactions_count_cache(pk):
    k = "notification_count_{0}".format(pk)
    if oth_db.get(k):
        oth_db.incr(k)
    else:
        oth_db.set(k, 0, timeout=None)


def up_all_click_count(pk):
    """更新某视频的点击数"""
    k='all_click_count_of_{0}'.format(pk)
    if cache_count.get(k):
        cache_count.incr(k)
        return cache_count.get(k)
    else:
        cache_count.set(k,1,timeout=None)
        return 1


def get_all_click_count(pk):
    """查看视频点击次数"""
    k = 'all_click_count_of_{0}'.format(pk)
    if cache_count.get(k):
        return cache_count.get(k)
    else:
        cache_count.set(k, 0, timeout=None)
        return 0

def up_all_share_count(pk):
    """更新分享次数"""
    k='all_share_count_of_{}'.format(pk)
    if cache_count.get(k):
        cache_count.incr(k)
        return cache_count.get(k)
    else:
        cache_count.set(k,1,timeout=None)
        return 1


def get_all_share_count(pk):
    """获取分享次数"""
    k = 'all_share_count_of_{}'.format(pk)
    if cache_count.get(k):
        return cache_count.get(k)
    else:

        return 0


def clear():
    cache_hour.clear()
    # pass


def update_hour_click(pk, omg):
    """更新小时点击数（暂时弃用）"""
    k = "CLICKS_{0}_{1}".format(omg, pk)
    if cache_hour.has_key(k):
        cache_hour.incr(k)
        # run_timer()
        # REDIS_DB.sadd("1:follow","9")

        return cache_hour.get(k)

    else:
        post = AllSongMusic.objects.get(pk=pk)
        cache_hour.set(k, post.hour_count + 1,timeout=None)
        # cache.persist(k)

        return cache_hour.get(k)


def get_hour_click(pk, omg):
    """获取小时点击数（弃用暂时）"""
    k = "CLICKS_{0}_{1}".format(omg, pk)
    if cache_hour.has_key(k):
        return cache_hour.get(k)
    else:
        # post=AllSongMusic.objects.get(pk=pk)
        cache_hour.set(k, 0,timeout=None)
        # cache.persist(k)
        return 0


def sync_click():
    """同步文章点击数（弃用暂时）"""
    print('同步点击数start....')


    if cache_hour.keys('CLICKS_allmusic*'):

        for k in cache_hour.keys('CLICKS_allmusic*'):
            try:
                music_id = str(k).split("_")[2]
                p = AllSongMusic.objects.get(pk=int(music_id))
                cache_click = get_click(music_id, 'allmusic')
                view_count = p.view_count
                hour_count = p.hour_count
                p.view_count = view_count + hour_count
                p.hour_count = cache_click

                p.save()

            except:
                pass
        clear()
    else:
        p = AllSongMusic.objects.all()
        for k in p:
            k.hour_count = 0
            k.save()
            # clear()
    print('同步文章点击数end....')
    global RUNNING_TIMER
    RUNNING_TIMER = False
