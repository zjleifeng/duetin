#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: praiseship.py
@time: 2017/7/14 下午6:49
@SOFTWARE:PyCharm
"""
import redis
from khufu.settings import redis_host
local_key_list = {
    "loveing": "loveing",
    "lovedby": "lovedby",
}
class Praiseship(object):

    def __init__(self, redis_connection=None, key_list=None, actor=None):

        if key_list:
            self.key_list = local_key_list.copy()
            self.key_list.update(key_list)
        else:
            self.key_list = local_key_list

        if redis_connection:
            self.redis_connection = redis_connection
        else:
            self.redis_connection = redis.StrictRedis(
                host=redis_host,
                port=6379,
                db=5
            )

        self.actor = actor

    def __call__(self, *args, **kwargs):

        self.actor = args[0]

        return self


    #赞
    def _action_call(self, command, from_id, to_id, operation_key):
        command_values = ':'.join(('praise', str(from_id), operation_key)), to_id
        return getattr(self.redis_connection, command)(*command_values)

    def _list_call(self, operation_key):
        return self.redis_connection.smembers(
            'praise:{}:{}'.format(self._get_actor(), operation_key)
        )

    def _count_call(self, operation_key):
        return self.redis_connection.scard(
            'praise:{}:{}'.format(
                self._get_actor(),
                operation_key
            )
        )

    def _get_actor(self):
        if hasattr(self, 'actor'):
            return self.actor

        raise ValueError("actor is not defined")


    def praise(self, to_id):

        self._action_call('sadd', self._get_actor(), to_id, self.key_list["loveing"])
        self._action_call('sadd', to_id, self._get_actor(), self.key_list["lovedby"])

    def unpraise(self, to_id):

        self._action_call('srem', self._get_actor(), to_id, self.key_list["loveing"])
        self._action_call('srem', to_id, self._get_actor(), self.key_list["lovedby"])



    #查找赞过某个视频的人
    def lovedby(self):
        return self._list_call(self.key_list["lovedby"])

    #查找某人赞过哪些视频
    def loveing(self):
        return self._list_call(self.key_list["loveing"])


    #查看某视频被赞多少次
    def lovedby_count(self):
        music_id = self.actor
        count = self._count_call(self.key_list["lovedby"])
        # if music_id == 11700:
        #     count = count + 105
        # elif music_id == 11725:
        #     count = count + 108
        # elif music_id == 11706:
        #     count = count + 138
        # elif music_id == 11742:
        #     count = count + 123
        # elif music_id == 11701:
        #     count = count + 145
        # elif music_id == 11739:
        #     count = count + 134
        # elif music_id == 11722:
        #     count = count + 124
        # elif music_id == 11747:
        #     count = count + 133
        # elif music_id == 11717:
        #     count = count + 121
        # elif music_id == 11713:
        #     count = count + 113
        # elif music_id == 11750:
        #     count = count + 143
        # elif music_id == 11756:
        #     count = count + 121
        # elif music_id == 11755:
        #     count = count + 122
        # elif music_id == 11752:
        #     count = count + 143
        return count

    #查看某人给出过多少次赞
    def loveing_count(self):
        return self._count_call(self.key_list["loveing"])



    #某视频是否被某人赞过
    def is_lovedby(self, lovedby_id):
        return self._action_call('sismember', self._get_actor(), lovedby_id, self.key_list["lovedby"])

    #某人是否赞过某视频
    def is_loveing(self, loveing_id):
        return self._action_call('sismember', self._get_actor(), loveing_id, self.key_list["loveing"])


