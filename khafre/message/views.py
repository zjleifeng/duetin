#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/7/17 下午2:08
@SOFTWARE:PyCharm
"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from khafre.utils.json_response import json_resp
from khafre.utils.pags import js_resp_paging
from relationships import Relationship
from khafre.main.cache_manager import up_notifactions_count, get_notifactions_count, del_notifactions_count
from app_auth.models import FollowerNotification,MobileVersion
from django.utils import timezone
import datetime
from django.core.cache import caches
from .serializers import Create_ExceptionCaseSerializer, FollowerNotificationSerializer, InviteSerializer, \
    AboutYouNotificationSerializer, Create_SongExceptionSerializer
from dao.models.music import Notification, AboutyouNotification
from khufu.settings import redis_ship
from khafre.utils.language import check_lan
r = Relationship(redis_ship)
oth_db = caches['oth']


# class Feed(APIView):
#     """
#     订阅API
#     """
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, format=None):
#         k = "notification_count_{0}".format(request.user.id)
#         notification_count = oth_db.get(k)
#
#         followers_id = list(r(request.user.id).following())
#         followers_list = []
#         followers_id.append(request.user.id)
#         all_music = AllSongMusic.objects.filter(all_music_auth__in=followers_id, is_enable=True,
#                                                 is_delete=False).order_by('-created_at')
#         if all_music:
#
#             return js_resp_paging(all_music, request, AllSongMusic_Feed_Serializer)
#         else:
#             return js_resp_paging(all_music, request, AllSongMusic_Feed_Serializer)


class Message_count_View(APIView):
    """
    OK
    2018/2/28
    获取用户消息数
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = self.request.user.id
        count = get_notifactions_count(user_id)
        return json_resp(code=200, msg='ok', data={"count": count})


class InviteView(APIView):
    """
    OK
    2018/2/28
    邀请消息
    XXX邀请 你 加入  url
    XXX与 你 合唱了 URL

    api/ve/notification/invited/            GET     type标识消息类型  2：邀请消息，1：加入合唱消息
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        current_time = timezone.localtime(timezone.now())
        accessible_time = current_time - datetime.timedelta(days=20)
        no_obj = Notification.objects.filter(to_user=request.user, is_delete=False,
                                             created_at__gt=accessible_time).order_by(
            '-created_at')
        del_notifactions_count(user.id)
        return js_resp_paging(no_obj, request, InviteSerializer)


class About_You_View(APIView):
    """
    ok
    2018/2/28
    关于你的消息
    api/ve/notification/you/            GET     type标识消息类型0：关注消息，1：评论消息，2：点赞消息
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        current_time = timezone.localtime(timezone.now())
        accessible_time = current_time - datetime.timedelta(days=20)
        objs = AboutyouNotification.objects.filter(to_user=user, is_delete=False,
                                                   created_at__gt=accessible_time).order_by('-created_at')

        return js_resp_paging(objs, request, AboutYouNotificationSerializer)


class FollowingView(APIView):
    """
    OK
    2018/2/28
    我关注的人的消息

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        current_time = timezone.localtime(timezone.now())
        accessible_time = current_time - datetime.timedelta(days=20)
        no_obj = FollowerNotification.objects.filter(to_user=user, is_delete=False,
                                                     created_at__gt=accessible_time).order_by(
            '-created_at')
        k = "notification_count_{0}".format(request.user.id)
        oth_db.set(k, 0, timeout=None)
        return js_resp_paging(no_obj, request, FollowerNotificationSerializer)


class ExceptionCaseView(APIView):
    """
    OK
    2018/2/28
    异常捕捉反馈信息接口"""
    permission_classes = (AllowAny,)

    def post(self, request):
        code_lag = check_lan(request)
        data = request.data
        data['case_user'] = request.user.id
        serializer = Create_ExceptionCaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return json_resp(code=200, msg='ok')
        return json_resp(code=499, msg=code_lag['499'])


class Song_Exception_View(APIView):
    """

    ok
    2018/2/28
    歌曲问题反馈接口
    POST
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code_lag = check_lan(request)
        date = request.data
        serializer = Create_SongExceptionSerializer(data=date)
        if serializer.is_valid():
            serializer.save()

            return json_resp(code=200, msg='OK')
        return json_resp(code=499, msg=code_lag['499'])


class ChangeCount(APIView):
    permission_classes=(AllowAny,)

    def get(self,request):
        from dao.models.music import PartSongMusic,MusicProfiel
        part_music=PartSongMusic.objects.select_related().all()

        part_list=[]
        for part in part_music:
            music_id=part.music_info.id
            part_list.append(music_id)

        new_list=list(set(part_list))


        if new_list:
            for new in new_list:
                music_new=PartSongMusic.objects.filter(music_info__id=new)
                count=music_new.count()
                change_music=MusicProfiel.objects.get(id=new)
                change_music.view_count=count
                change_music.save()
        return json_resp(code=200,msg='ok')