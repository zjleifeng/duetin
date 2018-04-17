# #!/usr/bin/env python
# # encoding: utf-8
#
# """
# @author: zj
# @site  :
# @file: serializers.py
# @time: 2017/6/12 下午12:22
# @SOFTWARE:PyCharm
# """
# from rest_framework import serializers
# from app_auth.models import NotificationApp, FollowerNotification
# from dao.models.music import AllSongMusic
#
# # from notifications.models import Notification
#
#
# class NotificationHQSerializer(serializers.ModelSerializer):
#     # msg = serializers.SerializerMethodField()
#
#     class Meta:
#         model = NotificationApp
#         fields = ('__all__')
#         # depth=2
#
#
# class FollowerNotificationSerializer(serializers.ModelSerializer):
#     # allmusic_post = serializers.SerializerMethodField()
#
#     class Meta:
#         model = FollowerNotification
#         fields = (
#         'id', 'title', 'text', 'link', 'from_user', 'action_user', 'post', 'to_user', 'type', 'is_read', 'created_at',
#         'is_delete')
#
#     # def get_allmusic_post(self, obj):
#     #     return AllSongMusic.objects.get(id=obj.post)
