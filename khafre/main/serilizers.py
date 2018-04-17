#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: serilizers.py.py
@time: 2017/4/12 下午7:22
@SOFTWARE:PyCharm
"""
from rest_framework import serializers
from dao.models.music import AllSongMusic, ALLComment, Singer, MusicProfiel, PartSongMusic, PartComment, \
    ReportSong, AllMusicCategory
from django.core.cache import caches

RUNNING_TIMER = False
from dao.models.base import PostData
from .cache_manager import get_all_click_count, get_all_share_count
from khafre.utils.praiseship import Praiseship
from django.utils import timezone
from rest_framework.authtoken.models import Token
import pytz
import random
p = Praiseship()
oth_db = caches['oth']
cache_count = caches["count"]
cache_hour = caches['hour_count']

from khufu.settings import onegif_url, onejpg_url, allgif_url, partplay_url, chorusplay_url, musicimg_url, userpic_url,hc_mp3_url

utc = pytz.utc
tz = pytz.timezone("Asia/Shanghai")
class DateTimeFieldWihTZ(serializers.DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class SingerSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27

    歌手信息ser
    """

    class Meta:
        model = Singer
        fields = ('id', 'singer_name',)


class MusicProfileSingerSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    歌曲信息 包含歌手信息 ser

    """

    singer = SingerSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = MusicProfiel
        fields = ('id', 'music_name', 'image', 'singer', 'is_online', 'is_loved')

    def get_image(self, obj):
        if obj.bucket_image_key:
            return musicimg_url + obj.bucket_image_key
        else:
            return obj.image


class MusicHtmlSerializer(serializers.ModelSerializer):
    """
        OK
        2018/2/27
        歌曲信息 后台管理页面 ser
        """
    singer = SingerSerializer(many=True, read_only=True)
    # view_count = serializers.SerializerMethodField()
    music_style = serializers.SerializerMethodField()

    part_a_count = serializers.SerializerMethodField()
    part_b_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = MusicProfiel
        fields = (
            'id', 'music_name', 'image', 'singer', 'uid', 'rank', 'sort', 'new_sort', 'top_rank', 'style',
            'music_style','view_count',
            'is_loved', 'part_a_count', 'part_b_count',
            'is_online', 'bucket_lyrics_key', 'bucket_accompany_key', 'segments_key_name')

    # def get_view_count(self, obj):
    #     count = get_all_click_count(obj.id)
    #     return count

    def get_image(self, obj):
        if obj.bucket_image_key:
            return musicimg_url + obj.bucket_image_key
        else:
            return obj.image

    def get_part_a_count(self, obj):
        i = 0
        part = obj.music_part.all()
        for p in part:
            if p.part == 0:
                i += 1
        return i

    def get_part_b_count(self, obj):
        i = 0
        part = obj.music_part.all()
        for p in part:
            if p.part == 1:
                i += 1
        return i

    def get_music_style(self, obj):
        if obj.style == 0:
            music_style = 'MELODY'
        elif obj.style == 1:
            music_style = "RAP"
        elif obj.style == 2:
            music_style = "Rap&Melody"
        else:
            music_style = 'Undefined'

        return music_style

    def update(self, instance, validated_data):
        instance.sort = validated_data.get('sort', instance.sort)
        instance.new_sort = validated_data.get('new_sort', instance.new_sort)
        instance.style = validated_data.get('style', instance.style)
        instance.is_loved = validated_data.get('is_loved', instance.is_loved)
        instance.top_rank = validated_data.get('top_rank', instance.top_rank)
        instance.is_online = validated_data.get('is_online', instance.is_online)
        instance.view_count=validated_data.get('view_count',instance.view_count)
        instance.save()
        return instance


class MusicProfileSearchSer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    歌曲信息 搜索页面搜索歌曲信息 ser
    """

    singer = SingerSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = MusicProfiel
        fields = (
            'id', 'music_name', 'image', 'singer')

    def get_image(self, obj):
        if obj.bucket_image_key:
            return musicimg_url + obj.bucket_image_key
        else:
            return obj.image


# class MusicProfielSerializer(serializers.ModelSerializer):
#
#     """
#     废弃
#     """
#     singer = SingerSerializer(many=True, read_only=True)
#     image = serializers.SerializerMethodField()
#
#     class Meta:
#         model = MusicProfiel
#         fields = (
#             'id', 'music_name', 'image', 'singer', 'style', 'language', 'Original_file', 'accompany',
#             'k_game', 'lyrics')
#
#
#     def get_image(self, obj):
#         if obj.bucket_image_key:
#             return musicimg_url + obj.bucket_image_key
#         else:
#             return obj.image

class CreatePartSongSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    part部分新建信息ser
    """

    class Meta:
        model = PartSongMusic
        fields = ("__all__")

    def create(self, validated_data):
        return PartSongMusic.objects.create(**validated_data)


# class PartSongMusicSerializer(serializers.ModelSerializer):
#
#     """
#     废弃
#     """
#     lyrics = serializers.ReadOnlyField(source='music_info.lyrics')
#     user_name = serializers.ReadOnlyField(source='music_auth.username')
#     user_picture = serializers.ReadOnlyField(source='music_auth.picture')
#
#     class Meta:
#         model = PartSongMusic
#         fields = (
#             'id', 'lyrics',
#             'user_name', 'user_picture')
#
#     def create(self, validated_data):
#         return PartSongMusic.objects.create(**validated_data)

class ALLCommentSerializers(serializers.ModelSerializer):
    """
        OK
        2018/2/27
        新建歌曲评论部分ser
    """

    class Meta:
        model = ALLComment
        fields = ("id", "text")

    def create(self, validated_data):
        return ALLComment.objects.create(**validated_data)


class FilteredIsdelListSerializer(serializers.ListSerializer):
    """查询集过滤is_delete=flase"""

    def to_representation(self, data):
        data = data.filter(is_delete=False)
        return super(FilteredIsdelListSerializer, self).to_representation(data)


class FilteredIsEnableListSerializer(serializers.ListSerializer):
    """查询集过滤is_delete=flase"""

    def to_representation(self, data):
        data = data.filter(is_delete=False, is_enable=True)
        return super(FilteredIsEnableListSerializer, self).to_representation(data)


class AllSongMusicDetailSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    查看单个合唱视频
    """
    music_name = serializers.ReadOnlyField(source='music_info.music_name')
    auth_part_userid = serializers.ReadOnlyField(source='music_auth_part.music_auth.id')
    auth_part_username = serializers.ReadOnlyField(source='music_auth_part.music_auth.username')
    auth_part_tx = serializers.SerializerMethodField()
    auth_part_jpg=serializers.SerializerMethodField()
    auth_part_resume=serializers.SerializerMethodField()
    participant_part_userid = serializers.ReadOnlyField(source='music_participant_part.music_auth.id')
    participant_username = serializers.ReadOnlyField(source='music_participant_part.music_auth.username')
    participant_part_tx = serializers.SerializerMethodField()
    participant_part_jpg = serializers.SerializerMethodField()
    participant_part_resume = serializers.SerializerMethodField()

    music_info = serializers.SerializerMethodField()
    # created_at = DateTimeFieldWihTZ()
    photo = serializers.SerializerMethodField()
    vedio = serializers.SerializerMethodField()

    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'title', 'music_info', 'photo', 'vedio', 'music_name', 'auth_part_userid', 'auth_part_username',
            'auth_part_tx','auth_part_jpg','auth_part_resume',
            'participant_part_userid', 'participant_username', 'participant_part_tx','participant_part_jpg','participant_part_resume', 'created_at')

    def get_music_info(self, obj):
        id = obj.music_info
        ser = MusicProfileSingerSerializer(id)
        return ser.data

    def get_auth_part_jpg(self,obj):
        if obj.music_auth_part:

            jpg_key=obj.music_auth_part.one_jpg_key
            if jpg_key:
                jpg_url=onejpg_url+jpg_key
                return jpg_url
            else:
                return None
        else:
            return None



    def get_participant_part_jpg(self,obj):
        if obj.music_participant_part:

            jpg_key=obj.music_participant_part.one_jpg_key
            if jpg_key:
                jpg_url=onejpg_url+jpg_key
                return jpg_url
            else:
                return None
        else:
            return None

    def get_photo(self, obj):
        if obj.photo_key_name:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "out_jpg/" + obj.photo_key_name
            else:
                return partplay_url + "out_jpg/" + obj.photo_key_name
        else:
            return None

    def get_vedio(self, obj):
        if obj.bucket_all_vedio_key:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
            else:
                return partplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
        else:
            return None

    def get_auth_part_tx(self, obj):
        if obj.music_auth_part:

            if obj.music_auth_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_auth_part.music_auth.picture_key_name
            else:
                if obj.music_auth_part.music_auth.picture:
                    pic = obj.music_auth_part.music_auth.picture
                else:
                    pic = ''

        else:
            pic = None
        return pic

    def get_auth_part_resume(self,obj):
        if obj.music_auth_part:
            if obj.music_auth_part.music_auth:
                resume=obj.music_auth_part.music_auth.resume
                return resume
            else:
                return None
        else:
            return None

    def get_participant_part_resume(self,obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth:
                resume=obj.music_participant_part.music_auth.resume
                return resume
            else:
                return None
        else:
            return None

    def get_participant_part_tx(self, obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_participant_part.music_auth.picture_key_name
            else:
                if obj.music_participant_part.music_auth.picture:
                    pic = obj.music_participant_part.music_auth.picture
                else:
                    pic = ''
            return pic
        else:
            return None


class AllSongMusicSearchSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    搜索歌曲，点击歌曲显示搜索结果 ser
    """
    view_count = serializers.SerializerMethodField()
    praise_count = serializers.SerializerMethodField()
    is_praise = serializers.SerializerMethodField()
    # created_at = DateTimeFieldWihTZ()
    photo = serializers.SerializerMethodField()
    vedio = serializers.SerializerMethodField()

    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'title', 'photo',
            'vedio', 'praise_count', 'view_count', 'created_at', 'is_praise')

    def get_praise_count(self, obj):
        redis_count = p(obj.id).lovedby_count()
        count=redis_count+obj.praise
        return count

    def get_view_count(self, obj):
        count = get_all_click_count(obj.id)
        return count

    def get_is_praise(self, obj):

        user = self.context['request'].user
        if p(user.id).is_loveing(obj.id):
            return True
        else:
            return False

    def get_photo(self, obj):
        if obj.all_gif_key:
            return allgif_url + obj.all_gif_key
        else:
            return ""

    def get_vedio(self, obj):
        if obj.bucket_all_vedio_key:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
            else:
                return partplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
        else:
            return ""


class AllSongMusicRecommendSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    推荐给新用户的视频列表
    """

    all_gif_url = serializers.SerializerMethodField()

    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'all_gif_url')

    def get_all_gif_url(self, obj):
        if obj.all_gif_key:
            return allgif_url + obj.all_gif_key
        else:
            return ""


class CreateAllSongMusicSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    新建合唱视频ser
    更新合唱视频 是否删除选项
    """

    class Meta:
        model = AllSongMusic
        fields = ("__all__")

    def create(self, validated_data):
        return AllSongMusic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        instance.deleted_at = validated_data.get('deleted_at', instance.deleted_at)
        instance.save()
        return instance


class ReportSongSerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    举报歌曲错误ser
    """

    class Meta:
        model = ReportSong
        fields = ('id', 'report_type', 'report_music', 'is_solve')

    def create(self, validated_data):
        return ReportSong.objects.create(**validated_data)


class AllSongMusic_Feed_Serializer(serializers.ModelSerializer):
    """
    ok
    2018/2/27
    订阅页面 我关注的人发布的视频
    """
    music_info = serializers.SerializerMethodField()
    auth_part_userid = serializers.ReadOnlyField(source='music_auth_part.music_auth.id')
    auth_part_username = serializers.ReadOnlyField(source='music_auth_part.music_auth.username')
    auth_part_tx = serializers.SerializerMethodField()
    auth_part_jpg = serializers.SerializerMethodField()
    auth_part_resume = serializers.SerializerMethodField()
    participant_part_userid = serializers.ReadOnlyField(source='music_participant_part.music_auth.id')
    participant_part_username = serializers.ReadOnlyField(source='music_participant_part.music_auth.username')
    participant_part_tx = serializers.SerializerMethodField()
    participant_part_jpg = serializers.SerializerMethodField()
    participant_part_resume = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    praise_count = serializers.SerializerMethodField()
    is_praise = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    # created_at = DateTimeFieldWihTZ()
    photo = serializers.SerializerMethodField()
    vedio = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'title', 'music_info', 'auth_part_userid', 'auth_part_username', 'auth_part_username',
            'auth_part_tx', 'photo', 'participant_part_userid', 'participant_part_username', 'participant_part_tx',
            'vedio', 'rank', 'comments', 'share_count', 'praise_count', 'view_count', 'comment_count', 'created_at',
            'is_praise','auth_part_jpg','auth_part_resume','participant_part_jpg','participant_part_resume')

    def get_comment_count(self, obj):
        return obj.all_music_comment.count()

    def get_music_info(self, obj):
        id = obj.music_info
        ser = MusicProfileSingerSerializer(id)

        return ser.data

    def get_praise_count(self, obj):
        redis_count = p(obj.id).lovedby_count()
        count = redis_count + obj.praise
        return count

    def get_view_count(self, obj):
        count = get_all_click_count(obj.id)
        return count

    def get_share_count(self, obj):
        count = get_all_share_count(obj.id)
        return count

    def get_is_praise(self, obj):

        user = self.context['request'].user
        if p(user.id).is_loveing(obj.id):
            return True
        else:
            return False

    def get_photo(self, obj):
        if obj.photo_key_name:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "out_jpg/" + obj.photo_key_name
            else:
                return partplay_url + "out_jpg/" + obj.photo_key_name
        else:
            return ""

    def get_vedio(self, obj):
        if obj.bucket_all_vedio_key:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
            else:
                return partplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
        else:
            return ""

    def get_auth_part_tx(self, obj):
        if obj.music_auth_part:

            if obj.music_auth_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_auth_part.music_auth.picture_key_name
            else:
                if obj.music_auth_part.music_auth.picture:
                    pic = obj.music_auth_part.music_auth.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic

    def get_participant_part_tx(self, obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_participant_part.music_auth.picture_key_name
            else:
                if obj.music_participant_part.music_auth.picture:
                    pic = obj.music_participant_part.music_auth.picture
                else:
                    pic = ''
            return pic
        else:
            return None

    def get_comments(self, obj):

        music_id = obj.id
        comments = ALLComment.objects.filter(music_id=music_id)[:6]
        li = []
        for com in comments:
            di = {}
            di['user_id'] = com.owner.id
            di["user"] = com.owner.username
            di['comment'] = com.text
            li.append(di)
        return li


    def get_auth_part_jpg(self,obj):
        if obj.music_auth_part:

            jpg_key=obj.music_auth_part.one_jpg_key
            if jpg_key:
                jpg_url=onejpg_url+jpg_key
                return jpg_url
            else:
                return None
        else:
            return None



    def get_participant_part_jpg(self,obj):
        if obj.music_participant_part:

            jpg_key=obj.music_participant_part.one_jpg_key
            if jpg_key:
                jpg_url=onejpg_url+jpg_key
                return jpg_url
            else:
                return None
        else:
            return None

    def get_auth_part_resume(self,obj):
        if obj.music_auth_part:
            if obj.music_auth_part.music_auth:
                resume=obj.music_auth_part.music_auth.resume
                return resume
            else:
                return None
        else:
            return None

    def get_participant_part_resume(self,obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth:
                resume=obj.music_participant_part.music_auth.resume
                return resume
            else:
                return None
        else:
            return None


class AllSongMusic_Popular_Serializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    主页请求 我已经他人发布的视频 返回数据序列化
    """
    comment_count = serializers.SerializerMethodField()
    music_info = serializers.SerializerMethodField()
    auth_part_userid = serializers.ReadOnlyField(source='music_auth_part.music_auth.id')
    auth_part_username = serializers.ReadOnlyField(source='music_auth_part.music_auth.username')
    auth_part_tx = serializers.SerializerMethodField()
    auth_part_jpg = serializers.SerializerMethodField()
    auth_part_resume = serializers.SerializerMethodField()
    participant_part_userid = serializers.ReadOnlyField(source='music_participant_part.music_auth.id')
    participant_part_username = serializers.ReadOnlyField(source='music_participant_part.music_auth.username')
    participant_part_tx = serializers.SerializerMethodField()
    participant_part_jpg = serializers.SerializerMethodField()
    participant_part_resume = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    praise_count = serializers.SerializerMethodField()
    is_praise = serializers.SerializerMethodField()
    # created_at = DateTimeFieldWihTZ()
    photo = serializers.SerializerMethodField()
    all_gif_url = serializers.SerializerMethodField()
    vedio = serializers.SerializerMethodField()

    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'title', 'music_info', 'auth_part_userid', 'auth_part_username','auth_part_jpg','auth_part_resume',
            'auth_part_tx', 'participant_part_userid', 'participant_part_username', 'participant_part_tx', 'photo',
            'all_gif_url','participant_part_jpg','participant_part_resume',
            'vedio', 'rank', 'share_count', 'praise_count', 'view_count', 'comment_count', 'created_at', 'is_praise')
        depth = 2

    def get_comment_count(self, obj):
        return obj.all_music_comment.count()

    def get_photo(self, obj):
        if obj.photo_key_name:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "out_jpg/" + obj.photo_key_name
            else:
                return partplay_url + "out_jpg/" + obj.photo_key_name
        else:
            return ""

    def get_vedio(self, obj):
        if obj.bucket_all_vedio_key:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
            else:
                return partplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
        else:
            return ""

    def get_all_gif_url(self, obj):
        if obj.all_gif_key:
            return allgif_url + obj.all_gif_key
        else:
            return ""

    def get_music_info(self, obj):
        id = obj.music_info
        ser = MusicProfileSingerSerializer(id)

        return ser.data

    def get_praise_count(self, obj):
        redis_count = p(obj.id).lovedby_count()
        count = redis_count + obj.praise
        return count

    def get_view_count(self, obj):
        count = get_all_click_count(obj.id)
        return count

    def create(self, validated_data):
        return AllSongMusic.objects.create(**validated_data)

    def get_share_count(self, obj):
        count = get_all_share_count(obj.id)
        return count

    def get_is_praise(self, obj):

        user = self.context['request'].user
        if p(user.id).is_loveing(obj.id):
            return True
        else:
            return False

    def get_auth_part_tx(self, obj):
        if obj.music_auth_part:

            if obj.music_auth_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_auth_part.music_auth.picture_key_name
            else:
                if obj.music_auth_part.music_auth.picture:
                    pic = obj.music_auth_part.music_auth.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic

    def get_participant_part_tx(self, obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_participant_part.music_auth.picture_key_name
            else:
                if obj.music_participant_part.music_auth.picture:
                    pic = obj.music_participant_part.music_auth.picture
                else:
                    pic = ''
            return pic
        else:
            return None

    def get_auth_part_jpg(self,obj):
        if obj.music_auth_part:

            jpg_key=obj.music_auth_part.one_jpg_key
            if jpg_key:
                jpg_url=onejpg_url+jpg_key
                return jpg_url
            else:
                return None
        else:
            return None



    def get_participant_part_jpg(self,obj):
        if obj.music_participant_part:

            jpg_key=obj.music_participant_part.one_jpg_key
            if jpg_key:
                jpg_url=onejpg_url+jpg_key
                return jpg_url
            else:
                return None
        else:
            return None

    def get_auth_part_resume(self,obj):
        if obj.music_auth_part:
            if obj.music_auth_part.music_auth:
                resume=obj.music_auth_part.music_auth.resume
                return resume
            else:
                return None
        else:
            return None

    def get_participant_part_resume(self,obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth:
                resume=obj.music_participant_part.music_auth.resume
                return resume
            else:
                return None
        else:
            return None


class AllSongMusic_html5_Serializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    分享页面SER
    """
    is_chorus = serializers.SerializerMethodField()
    music_info = serializers.SerializerMethodField()
    auth_part_userid = serializers.ReadOnlyField(source='all_music_auth.id')
    auth_part_username = serializers.ReadOnlyField(source='all_music_auth.username')
    auth_part_tx = serializers.SerializerMethodField()
    participant_part_userid = serializers.ReadOnlyField(source='music_participant_part.music_auth.id')
    participant_part_username = serializers.ReadOnlyField(source='music_participant_part.music_auth.username')
    participant_part_tx = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    vedio = serializers.SerializerMethodField()
    app_share_jpg = serializers.SerializerMethodField()
    h5_share_jpg = serializers.SerializerMethodField()

    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'title', 'app_share_jpg', 'h5_share_jpg', 'is_chorus', 'music_info', 'auth_part_userid',
            'auth_part_username',
            'auth_part_tx', 'participant_part_userid', 'participant_part_username', 'participant_part_tx',
            'vedio', 'created_time')
        depth = 2

    def get_app_share_jpg(self, obj):
        if obj.share_jpg_key:
            photo_key = obj.share_jpg_key
            photo_url = chorusplay_url + "out_jpg/" + photo_key
        else:
            photo_url = chorusplay_url + "out_jpg/default.jpg"
        return photo_url

    def get_music_info(self, obj):
        id = obj.music_info
        ser = MusicHtmlSerializer(id)
        data = {}
        data['music_name'] = ser.data["music_name"]
        data['singer'] = ser.data['singer']

        return data

    def get_is_chorus(self, obj):
        if obj.music_participant_part:
            return True
        else:
            return False

    def get_h5_share_jpg(self, obj):
        if obj.photo_key_name:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "out_jpg/" + obj.photo_key_name
            else:
                return partplay_url + "out_jpg/" + obj.photo_key_name
        else:
            return ""

    def get_vedio(self, obj):
        if obj.bucket_all_vedio_key:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
            else:
                return partplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
        else:
            return ""

    def get_created_time(self, obj):
        # localLoginTime = timezone.localtime(obj.created_at)
        # 格式化时间 strftime 由time对象调用
        # localLoginTime = localLoginTime.strftime("%Y-%m-%d %H:%M:%S")
        return obj.created_at

    def get_auth_part_tx(self, obj):
        if obj.music_auth_part:

            if obj.music_auth_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_auth_part.music_auth.picture_key_name
            else:
                if obj.music_auth_part.music_auth.picture:
                    pic = obj.music_auth_part.music_auth.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic

    def get_participant_part_tx(self, obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_participant_part.music_auth.picture_key_name
            else:
                if obj.music_participant_part.music_auth.picture:
                    pic = obj.music_participant_part.music_auth.picture
                else:
                    pic = ''
            return pic
        else:
            return None


class AllSongMusic_htm_Serializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    运营管理合唱歌曲ser
    """
    comment_count = serializers.SerializerMethodField()
    music_info = serializers.SerializerMethodField()
    auth_part_userid = serializers.ReadOnlyField(source='all_music_auth.id')
    auth_part_username = serializers.ReadOnlyField(source='all_music_auth.username')
    auth_part = serializers.SerializerMethodField()
    participant_part = serializers.SerializerMethodField()
    participant_part_userid = serializers.ReadOnlyField(source='music_participant_part.music_auth.id')
    participant_part_username = serializers.ReadOnlyField(source='music_participant_part.music_auth.username')
    participant_part_tx = serializers.SerializerMethodField()
    auth_part_tx = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    praise_count = serializers.SerializerMethodField()
    is_praise = serializers.SerializerMethodField()
    h_rating_scale = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    vedio = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()


    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'title', 'photo', 'music_info', 'auth_part_userid', 'auth_part_username',
            'auth_part_tx', 'participant_part_userid', 'participant_part_username', 'participant_part_tx',
            'vedio', 'rank', 'view_count_rank', 'share_count', 'praise_count', 'view_count', 'comment_count',
            'created_time', 'is_praise', 'rating_scale', 'h_rating_scale', 'is_enable', 'is_recommend_rank',
            'participant_part', 'auth_part', 'all_category', 'category','praise')
        depth = 2

    def get_category(self, obj):
        if obj.all_category:
            return obj.all_category.name
        else:
            return "未分类"

    def get_auth_part(self, obj):
        if obj.music_auth_part:
            part_id = obj.music_auth_part
        else:
            part_id = None
        if part_id:
            part = part_id.part
            if part == 1:
                return "B"
            else:
                return 'A'
        else:
            return "unknow"

    def get_participant_part(self, obj):
        part_id = obj.music_participant_part
        if part_id:
            part = part_id.part
            if part == 1:
                return "B"
            else:
                return 'A'
        else:
            return "unknow"

    def get_comment_count(self, obj):
        return obj.all_music_comment.count()

    def get_music_info(self, obj):
        id = obj.music_info
        ser = MusicHtmlSerializer(id)

        return ser.data

    def get_praise_count(self, obj):
        redis_count = p(obj.id).lovedby_count()
        count = redis_count + obj.praise
        return count

    def get_view_count(self, obj):
        count = get_all_click_count(obj.id)
        return count

    def create(self, validated_data):
        return AllSongMusic.objects.create(**validated_data)

    def get_share_count(self, obj):
        count = get_all_share_count(obj.id)
        return count

    def get_is_praise(self, obj):

        user = self.context['request'].user
        if p(user.id).is_loveing(obj.id):
            return True
        else:
            return False

    def get_h_rating_scale(self, obj):
        if obj.rating_scale == 1:
            h_rating_scale = "A"
        elif obj.rating_scale == 2:
            h_rating_scale = 'B'
        elif obj.rating_scale == 3:
            h_rating_scale = 'C'
        elif obj.rating_scale == 4:
            h_rating_scale = 'D'
        elif obj.rating_scale == 5:
            h_rating_scale = 'E'
        else:
            h_rating_scale = 'unknow'
        return h_rating_scale

    def get_created_time(self, obj):
        # localLoginTime = timezone.localtime(obj.created_at)
        # 格式化时间 strftime 由time对象调用
        # localLoginTime = localLoginTime.strftime("%Y-%m-%d %H:%M:%S")
        return obj.created_at

    def get_photo(self, obj):
        if obj.photo_key_name:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "out_jpg/" + obj.photo_key_name
            else:
                return partplay_url + "out_jpg/" + obj.photo_key_name
        else:
            return ""

    def get_vedio(self, obj):
        if obj.bucket_all_vedio_key:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
            else:
                return partplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
        else:
            return ""

    def get_auth_part_tx(self, obj):
        if obj.music_auth_part:

            if obj.music_auth_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_auth_part.music_auth.picture_key_name
            else:
                if obj.music_auth_part.music_auth.picture:
                    pic = obj.music_auth_part.music_auth.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic

    def get_participant_part_tx(self, obj):
        if obj.music_participant_part:
            if obj.music_participant_part.music_auth.picture_key_name:
                pic = userpic_url + obj.music_participant_part.music_auth.picture_key_name
            else:
                if obj.music_participant_part.music_auth.picture:
                    pic = obj.music_participant_part.music_auth.picture
                else:
                    pic = ''
            return pic
        else:
            return None

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.rank)
        instance.view_count_rank = validated_data.get('view_count_rank', instance.view_count_rank)
        instance.is_enable = validated_data.get('is_enable', instance.is_enable)
        instance.is_recommend_rank = validated_data.get('is_recommend_rank', instance.is_recommend_rank)
        instance.rating_scale = validated_data.get('rating_scale', instance.rating_scale)
        instance.all_category = validated_data.get('all_category', instance.all_category)
        instance.praise=validated_data.get('praise',instance.praise)
        instance.save()
        return instance


class PartRandomSerializer(serializers.ModelSerializer):
    all_music_id=serializers.SerializerMethodField()
    part_to=serializers.SerializerMethodField()
    auth_part_userid = serializers.ReadOnlyField(source='music_auth.id')
    auth_part_username = serializers.ReadOnlyField(source='music_auth.username')
    auth_part_tx = serializers.SerializerMethodField()
    auth_part_sex=serializers.ReadOnlyField(source='music_auth.sex')
    auth_part_birth=serializers.ReadOnlyField(source='music_auth.birth')
    music_info = serializers.SerializerMethodField()
    hc_aac_url=serializers.SerializerMethodField()
    play_time=serializers.SerializerMethodField()

    background_pic=serializers.SerializerMethodField()
    class Meta:
        model=PartSongMusic
        fields=('all_music_id','part_to','auth_part_userid','auth_part_username','auth_part_tx','background_pic','auth_part_sex','auth_part_birth','music_info','hc_aac_url','play_time')

    def get_part_to(self,obj):
        return 1

    def get_all_music_id(self,obj):
        all_music=AllSongMusic.objects.filter(music_auth_part=obj).first()
        return all_music.id

    def get_auth_part_tx(self, obj):
        if obj.music_auth:

            default_tx=obj.music_auth.picture_key_name

            if default_tx:
                pic =userpic_url+ default_tx
            else:
                if obj.music_auth.picture:
                    pic = obj.music_auth.picture
                else:

                    tx_key_list = ["def_tx_01.jpg", "def_tx_02.jpg", "def_tx_03.jpg", "def_tx_04.jpg", "def_tx_05.jpg",
                                   "def_tx_06.jpg",
                                   "def_tx_07.jpg", "def_tx_08.jpg", "def_tx_09.jpg", "def_tx_10.jpg"]
                    tx_key=random.choice(tx_key_list)
                    pic=userpic_url+tx_key

        else:
            pic = ""
        return pic

    def get_background_pic(self,obj):
        if obj.music_auth:
            bc=obj.music_auth.background_key_name
            if bc:
                pic=userpic_url+bc
            else:
                tx_key_list = ["def_tx_01.jpg", "def_tx_02.jpg", "def_tx_03.jpg", "def_tx_04.jpg", "def_tx_05.jpg",
                               "def_tx_06.jpg",
                               "def_tx_07.jpg", "def_tx_08.jpg", "def_tx_09.jpg", "def_tx_10.jpg"]
                tx_key = random.choice(tx_key_list)
                pic = userpic_url + tx_key
            return pic
        else:
            return ""

    def get_music_info(self, obj):
        id = obj.music_info
        ser = MusicProfileSearchSer(id)
        return ser.data

    def get_hc_aac_url(self,obj):
        aac_key=obj.hc_aac_key_name
        return hc_mp3_url+aac_key

    def get_play_time(self,obj):
        part=obj.part
        if part==0:
            return obj.music_info.time_a
        else:
            return obj.music_info.time_b

class PartSongMusic_htm_Serializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    运营管理part ser
    """
    music_info = serializers.SerializerMethodField()
    auth_part_userid = serializers.ReadOnlyField(source='music_auth.id')
    auth_part_username = serializers.ReadOnlyField(source='music_auth.username')
    auth_part_tx = serializers.SerializerMethodField()
    h_rating_scale = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = PartSongMusic
        fields = (
            'id', 'title', 'music_info', 'auth_part_userid', 'auth_part_username',
            'auth_part_tx', 'part', 'photo', 'vedio', 'part_vedio_url',
            'created_time', 'rating_scale', 'h_rating_scale', 'is_enable')

    def get_music_info(self, obj):
        id = obj.music_info
        ser = MusicHtmlSerializer(id)
        return ser.data


    def get_auth_part_tx(self, obj):
        if obj.music_auth:

            if obj.music_auth.picture_key_name:
                pic = userpic_url + obj.music_auth.picture_key_name
            else:
                if obj.music_auth.picture:
                    pic = obj.music_auth.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic

    def get_h_rating_scale(self, obj):
        if obj.rating_scale == 1:
            h_rating_scale = "A"
        elif obj.rating_scale == 2:
            h_rating_scale = 'B'
        elif obj.rating_scale == 3:
            h_rating_scale = 'C'
        elif obj.rating_scale == 4:
            h_rating_scale = 'D'
        elif obj.rating_scale == 5:
            h_rating_scale = 'E'
        else:
            h_rating_scale = 'unknow'
        return h_rating_scale

    def get_created_time(self, obj):
        # localLoginTime = timezone.localtime(obj.created_at)
        # # 格式化时间 strftime 由time对象调用
        # localLoginTime = localLoginTime.strftime("%Y-%m-%d %H:%M:%S")
        # return localLoginTime
        return obj.created_at

    def update(self, instance, validated_data):
        instance.is_enable = validated_data.get('is_enable', instance.is_enable)
        instance.rating_scale = validated_data.get('rating_scale', instance.rating_scale)
        instance.save()
        return instance


class All_comment_serializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    查看视频评论 ser
    """
    owner_id = serializers.ReadOnlyField(source='owner.id')
    owner_name = serializers.ReadOnlyField(source='owner.username')
    owner_picutre = serializers.SerializerMethodField()
    # created_at = DateTimeFieldWihTZ()

    class Meta:
        model = ALLComment
        fields = ('id', 'text', 'owner_id', 'owner_name', 'created_at', 'owner_picutre')

    def get_owner_picutre(self, obj):
        if obj.owner:

            if obj.owner.picture_key_name:
                pic = userpic_url + obj.owner.picture_key_name
            else:
                if obj.owner.picture:
                    pic = obj.owner.picture
                else:
                    pic = ''
        else:
            pic = ""
        return pic


class PostData_htm_Serializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    系统后台合唱歌曲的原始数据ser
    """
    part_id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    user_token = serializers.SerializerMethodField()
    aac_key = serializers.SerializerMethodField()
    mp4_key = serializers.SerializerMethodField()
    music_id = serializers.ReadOnlyField(source='music_info.id')
    # participant_id = serializers.ReadOnlyField(source='music_participant_part.id')
    part_to = serializers.SerializerMethodField()
    ts = serializers.SerializerMethodField()
    trim = serializers.SerializerMethodField()
    rating_scale=serializers.SerializerMethodField()
    participant_id=serializers.SerializerMethodField()
    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'photo', 'vedio', 'rating_scale','part_id', 'username', 'user_token', "aac_key", 'mp4_key', 'music_id',
            'participant_id',
            'part_to', 'title', 'ts', 'trim')


    def get_participant_id(self,obj):
        old_participant_id=obj.music_participant_part.id
        try:
            post_data=PostData.objects.get(old_part=old_participant_id)
            all_music_id=post_data.all_music_id

            all_music=AllSongMusic.objects.get(id=all_music_id)

            t_part_id=all_music.music_auth_part.id
            return t_part_id
        except:
            return 0

    def get_rating_scale(self,obj):
        if obj.music_auth_part:
            return obj.music_auth_part.rating_scale
        else:
            return ""

    def get_part_id(self, obj):
        if obj.music_auth_part:
            return obj.music_auth_part.id
        else:
            return 0

    def get_username(self, obj):
        if obj.all_music_auth:
            return obj.all_music_auth.username
        else:
            return "unknow error"

    def get_user_token(self, obj):
        if obj.all_music_auth:
            user_id = obj.all_music_auth.id
            token = Token.objects.get(user_id=user_id)
            return token.key
        else:
            return "unknow error"

    def get_aac_key(self, obj):
        if obj.music_auth_part:
            return obj.music_auth_part.aac_bucket_key
        else:
            return "unknow error"

    def get_mp4_key(self, obj):
        if obj.music_auth_part:
            return obj.music_auth_part.vedio_bucket_key
        else:
            return "unknow error"

    def get_part_to(self, obj):
        if obj.music_auth_part:
            return obj.music_auth_part.part
        else:
            return "unknow error"

    def get_ts(self, obj):
        uid = obj.music_auth_part.vedio_bucket_key
        postdata = PostData.objects.filter(mp4_key_name=uid).first()

        if postdata:
            ts = postdata.ts
        else:
            ts = 0
        return ts

    def get_trim(self, obj):

        if obj.all_music_auth.mobile:

            mobile_trim=obj.all_music_auth.mobile.delay_time
            if mobile_trim:
                return mobile_trim
            else:
                return 300
        else:
            # return 300
            uid = obj.music_auth_part.vedio_bucket_key
            postdata = PostData.objects.filter(mp4_key_name=uid).first()

            if postdata:
                trim = postdata.trim
                trim_ok = trim - 50
            else:
                trim_ok = 300

            return trim_ok


        # uid = obj.music_auth_part.vedio_bucket_key
        # postdata = PostData.objects.filter(mp4_key_name=uid).first()
        #
        # if postdata:
        #     trim = postdata.trim
        #     trim_ok = trim - 50
        # else:
        #     trim_ok = "unknow"
        #
        # return trim_ok


class CategorySerializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    搜索页下方，歌曲分类后台管理ser
    """

    class Meta:
        model = AllMusicCategory
        fields = ('id', 'name', 'rank', 'is_online')

    def create(self, validated_data):
        return AllMusicCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.is_online = validated_data.get('is_online', instance.is_online)
        instance.save()
        return instance


class All_Category_Serializer(serializers.ModelSerializer):
    """
    OK
    2018/2/27
    搜索页下方，歌曲分类 查看ser
    """
    all_category_video = AllSongMusicRecommendSerializer(many=True, read_only=True)
    name=serializers.SerializerMethodField()
    class Meta:
        model = AllMusicCategory
        fields = ('id', 'name', 'all_category_video')

    def get_name(self,obj):
        request = self.context['request']
        if request.META.has_key("HTTP_X_LOCALE"):
            lang = request.environ['HTTP_X_LOCALE']

            if lang == "id":
                return obj.id_name
            else:
                return obj.name

        else:
            return obj.name

class All_Songmusic_Manual_htm_Serializer(serializers.ModelSerializer):
    """
    2018/3/7
    运营页面手动合成合唱数据
    """
    photo = serializers.SerializerMethodField()
    vedio = serializers.SerializerMethodField()
    up_mp4_one = serializers.SerializerMethodField()
    up_aac_one = serializers.SerializerMethodField()
    trim_one = serializers.SerializerMethodField()
    up_mp4_two = serializers.SerializerMethodField()
    up_aac_two = serializers.SerializerMethodField()
    trim_two = serializers.SerializerMethodField()
    banzou = serializers.SerializerMethodField()
    time_json = serializers.SerializerMethodField()
    part_to = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = AllSongMusic
        fields = (
            'id', 'photo', 'vedio', 'up_mp4_one', 'up_aac_one', 'trim_one', 'up_mp4_two', 'up_aac_two',
            'trim_two', 'banzou', 'time_json', 'part_to', 'created_time')

    def get_photo(self, obj):
        if obj.photo_key_name:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "out_jpg/" + obj.photo_key_name
            else:
                return partplay_url + "out_jpg/" + obj.photo_key_name
        else:
            return ""

    def get_vedio(self, obj):
        if obj.bucket_all_vedio_key:
            bucket_cho = obj.bucket_all_vedio_name
            if bucket_cho == "duetin-chorus":
                return chorusplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
            else:
                return partplay_url + "compose_vedio/" + obj.bucket_all_vedio_key
        else:
            return ""

    def get_up_mp4_one(self, obj):

        vedio_key = obj.music_participant_part.vedio_bucket_key
        if vedio_key:
            return "https://s3-ap-southeast-1.amazonaws.com/duetin-android-upmp4/" + vedio_key
        else:
            return ""

    def get_up_aac_one(self, obj):
        aac_key = obj.music_participant_part.aac_bucket_key
        if aac_key:
            return "https://s3-ap-southeast-1.amazonaws.com/duetin-android-upaac/" + aac_key
        else:
            return ""

    def get_trim_one(self, obj):
        vedio_key = obj.music_participant_part.vedio_bucket_key
        post_part=PostData.objects.filter(uid=vedio_key).first()
        if post_part:
            trim=int(post_part.trim)-50
            return trim
        else:
            return ""
    def get_up_mp4_two(self, obj):
        vedio_key = obj.music_auth_part.vedio_bucket_key
        if vedio_key:
            return "https://s3-ap-southeast-1.amazonaws.com/duetin-android-upmp4/" + vedio_key
        else:
            return ""

    def get_up_aac_two(self, obj):
        aac_key = obj.music_auth_part.aac_bucket_key
        if aac_key:
            return "https://s3-ap-southeast-1.amazonaws.com/duetin-android-upaac/" + aac_key
        else:
            return ""

    def get_trim_two(self, obj):
        key_id = obj.id

        post_data = PostData.objects.filter(all_music_id=key_id).first()

        if post_data:
            trim = int(post_data.trim) - 50

            return trim
        else:
            return ""
    def get_banzou(self, obj):

        banzou_key = obj.music_info.bucket_accompany_key

        if banzou_key:
            return "https://s3-ap-southeast-1.amazonaws.com/duetin-accompany/" + banzou_key
        else:
            return ""

    def get_time_json(self, obj):
        sem_key = obj.music_info.segments_key_name

        if sem_key:
            return "https://s3-ap-southeast-1.amazonaws.com/duetin-segments/" + sem_key
        else:
            return ""

    def get_part_to(self,obj):
        key_id = obj.id
        post_data = PostData.objects.filter(all_music_id=key_id).first()
        if post_data:
            part_to=post_data.part_to
            if part_to:
                return "A/B"
            else:
                return "B/A"
        else:
            return ""
    def get_created_time(self, obj):
        # localLoginTime = timezone.localtime(obj.created_at)
        # 格式化时间 strftime 由time对象调用
        # localLoginTime = localLoginTime.strftime("%Y-%m-%d %H:%M:%S")
        return obj.created_at
