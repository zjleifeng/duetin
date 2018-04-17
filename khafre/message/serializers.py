#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: serializers.py
@time: 2017/7/17 下午2:08
@SOFTWARE:PyCharm
"""

from rest_framework import serializers
from dao.models.music import AboutyouNotification
from dao.models.music import Notification
from django.utils import timezone
from relationships import Relationship
from khufu.settings import redis_ship
from app_auth.models import FollowerNotification
from dao.models.base import ExceptionCase, SongException
from app_auth.models import MobileVersion
from khufu.settings import chorusplay_url, partplay_url,userpic_url,aac_url
import random
r = Relationship(redis_ship)


# from notifications.models import Notification
class DateTimeFieldWihTZ(serializers.DateTimeField):
    """UTC时间转换为时区时间"""

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class InviteSerializer(serializers.ModelSerializer):
    """
        OK
        2018/2/27
        邀请消息ser
    """
    form_user_id = serializers.ReadOnlyField(source='from_user.id')
    form_user_name = serializers.ReadOnlyField(source='from_user.username')
    form_user_tx = serializers.SerializerMethodField()
    to_user_id = serializers.ReadOnlyField(source='to_user.id')
    to_user_name = serializers.ReadOnlyField(source='to_user.username')
    to_user_tx = serializers.SerializerMethodField()
    post_id = serializers.ReadOnlyField(source='all_post.id')
    post_photo = serializers.SerializerMethodField()
    music_name = serializers.ReadOnlyField(source='all_post.music_info.music_name')
    created_at = DateTimeFieldWihTZ()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id', 'form_user_id', 'form_user_name', 'form_user_tx', 'to_user_id', 'to_user_name', 'to_user_tx', 'type',
            'post_id', 'link', 'music_name', 'post_photo', 'is_following', 'created_at')
        # depth=2

    def get_post_photo(self, obj):
        if obj.all_post.share_jpg_key:
            return chorusplay_url + "out_jpg/" + obj.all_post.share_jpg_key
        else:
            return ""

    def get_form_user_tx(self, obj):
        if obj.from_user:

            if obj.from_user.picture_key_name:
                pic = userpic_url + obj.from_user.picture_key_name
            else:
                if obj.from_user.picture:
                    pic = obj.from_user.picture
                else:
                    pic =''
        else:
            pic = ""
        return pic

    def get_to_user_tx(self, obj):
        if obj.to_user:

            if obj.to_user.picture_key_name:
                pic = userpic_url + obj.to_user.picture_key_name
            else:
                if obj.to_user.picture:
                    pic = obj.to_user.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic

    def get_is_following(self, obj):
        user = self.context['request'].user
        user_id = user.id
        if r(user_id).is_following(obj.from_user.id):
            return True
        else:
            return False


class AboutYouNotificationSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    关于你的消息ser
    """
    form_user_id = serializers.ReadOnlyField(source='from_user.id')
    form_user_name = serializers.ReadOnlyField(source='from_user.username')
    form_user_tx = serializers.SerializerMethodField()

    to_user_id = serializers.ReadOnlyField(source='to_user.id')
    to_user_name = serializers.ReadOnlyField(source='to_user.username')
    to_user_tx = serializers.SerializerMethodField()

    post_id = serializers.ReadOnlyField(source='all_post.id')
    music_name = serializers.ReadOnlyField(source='all_post.music_info.music_name')
    post_photo = serializers.SerializerMethodField()
    created_at = DateTimeFieldWihTZ()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = AboutyouNotification
        fields = (
            'id', 'form_user_id', 'form_user_name', 'form_user_tx', 'to_user_id', 'to_user_name', 'to_user_tx', 'type',
            'post_id', 'link', 'post_photo', 'music_name', 'is_following', 'created_at')

    def get_is_following(self, obj):
        user = self.context['request'].user
        user_id = user.id
        if r(user_id).is_following(obj.from_user.id):
            return True
        else:
            return False

    def get_post_photo(self, obj):
        try:
            share_jpg_key= obj.all_post.share_jpg_key
            return chorusplay_url + "out_jpg/" + share_jpg_key
        except:
            return ""

    def get_form_user_tx(self, obj):
        if obj.from_user:

            if obj.from_user.picture_key_name:
                pic = userpic_url + obj.from_user.picture_key_name
            else:
                if obj.from_user.picture:
                    pic = obj.from_user.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic

    def get_to_user_tx(self, obj):
        if obj.to_user:

            if obj.to_user.picture_key_name:
                pic = userpic_url + obj.to_user.picture_key_name
            else:
                if obj.to_user.picture:
                    pic = obj.to_user.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic


class Create_AboutyouNotificationSer(serializers.ModelSerializer):
    """
            OK
            2018/2/27
            新建关于你的消息ser
        """

    class Meta:
        model = AboutyouNotification
        fields = ("__all__")

    def create(self, validated_data):
        return AboutyouNotification.objects.create(**validated_data)


class FollowerNotificationSerializer(serializers.ModelSerializer):
    """
            OK
            2018/2/27
            我关注的人的消息ser
        """
    created_at = DateTimeFieldWihTZ()

    class Meta:
        model = FollowerNotification
        fields = (
            'id', 'title', 'text', 'link', 'from_user', 'action_user', 'post', 'to_user', 'type', 'is_read',
            'created_at',
            'is_delete')


class Create_FollowerNotificationSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    新建 我关注的人的消息ser
    """

    class Meta:
        model = FollowerNotification
        fields = ("__all__")

    def create(self, validated_data):
        return FollowerNotification.objects.create(**validated_data)


class Create_ExceptionCaseSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    异常消息 新建
    """

    class Meta:
        model = ExceptionCase
        fields = ("__all__")

    def create(self, validated_data):
        return ExceptionCase.objects.create(**validated_data)


class MobileVersionSer(serializers.ModelSerializer):
    """
        OK
        2018/2/27
        手机信息管理ser 新建 更新
    """

    part_aac=serializers.SerializerMethodField()

    class Meta:
        model = MobileVersion
        fields = ('id',"mobile_brand",'mobile_name','mobile_version','mobile_edition','mobile_yj_name','default_time','delay_time','part_aac')




    def get_part_aac(self,obj):
        users=obj.usermoblie.all()
        if users:
            music_list=[]
            for user in users:
                my_music=user.my_part_post.all()
                if my_music:
                    for x in my_music:
                        is_en=x.is_enable
                        if is_en:

                            music_list.append(x)
                        else:
                            pass
                else:
                    pass
            if music_list:
                part_music=music_list[:1][0]
                banzou=part_music.music_info.accompany
                aac_yp=aac_url + part_music.aac_bucket_key
                data={"banzou":banzou,"aac_yp":aac_yp}
                return data
            else:
                return ""
        else:
            return ""

    def create(self, validated_data):
        return MobileVersion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mobile_brand = validated_data.get('mobile_brand', instance.mobile_brand)
        instance.mobile_name = validated_data.get('mobile_name', instance.mobile_name)
        instance.mobile_version = validated_data.get('mobile_version', instance.mobile_version)
        instance.mobile_edition = validated_data.get('mobile_edition', instance.mobile_edition)
        instance.mobile_yj_name = validated_data.get('mobile_yj_name', instance.mobile_yj_name)
        instance.delay_time = validated_data.get('delay_time', instance.delay_time)

        instance.save()
        return instance


class Create_SongExceptionSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/28
    歌曲举报问题，新建更新，ser
    """

    h_case_option = serializers.SerializerMethodField()

    class Meta:
        model = SongException
        fields = ("id", 'song_name', 'singer_name', 'h_case_option', 'case_option', 'description', 'is_settle')

    def get_h_case_option(self, obj):
        if obj.case_option:
            if obj.case_option == 1:
                return "Cannot find song"
            else:
                return "Wrong research result"
        else:
            return ""

    def create(self, validated_data):
        return SongException.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_settle = validated_data.get('is_settle', instance.is_settle)
        instance.save()
        return instance
