#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/5/22 下午5:33
@SOFTWARE:PyCharm
"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from khafre.utils.json_response import json_resp, JsonResponse_zj
from khafre.utils.pags import api_paging, js_resp_paging, js_resp_newuser_paging
from app_auth.models import User, Fans
from dao.models.music import AllSongMusic
from khafre.main.serilizers import AllSongMusicSearchSerializer, AllSongMusic_Feed_Serializer
from relationships import Relationship
from django.http import JsonResponse
from django.db.models import Q
from dao.models.music import MusicProfiel
from khafre.utils.json_response import json_resp

from django.core.cache import cache, caches

from khufu.settings import redis_ship
from khafre.utils.language import check_lan

r = Relationship(redis_ship)

oth_db = caches['oth']


class Feed(APIView):
    """
    OK

    订阅API
    我关注的人发布的视频
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        followers_id = list(r(request.user.id).following())
        if followers_id:
            all_music = AllSongMusic.objects.filter(all_music_auth__in=followers_id, is_enable=True,
                                                    is_delete=False).order_by('-created_at')
            return js_resp_newuser_paging(all_music, request, AllSongMusic_Feed_Serializer, is_following=True, pages=10)

        else:

            all_music = AllSongMusic.objects.filter(Q(is_recommend_rank__gt=0), is_enable=True,
                                                    is_delete=False).order_by('-is_recommend_rank')
            return js_resp_newuser_paging(all_music, request, AllSongMusic_Feed_Serializer, is_following=False,
                                          pages=10)


class Music_Click_Count_View(APIView):
    """
    2018/3/8
    歌曲点击一次则计数加1
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code_lag = check_lan(request)
        try:

            music_id = request.data.get('musicid')
        except:
            return json_resp(code=499, msg=code_lag['499'])
        if music_id:
            try:
                music = MusicProfiel.objects.get(id=music_id)
                music.view_count += 1
                music.save()
                return json_resp(code=200, msg="ok")
            except:
                return json_resp(code=499, msg=code_lag['499'])
        else:
            return json_resp(code=499, msg=code_lag['499'])