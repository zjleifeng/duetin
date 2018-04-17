#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/3/30 下午1:55
@SOFTWARE:PyCharm
"""
from app_auth.models import User
from serilizers import SingerSerializer, ALLCommentSerializers, \
    AllSongMusicSearchSerializer, AllSongMusic_Popular_Serializer, AllSongMusicDetailSerializer, \
    CreateAllSongMusicSerializer, \
    All_comment_serializer, MusicProfileSearchSer, AllSongMusic_html5_Serializer, AllSongMusicRecommendSerializer, \
    All_Category_Serializer
from app_auth.serializers import AccountSerializer
from dao.models.music import Singer, AllSongMusic, ALLComment, MusicProfiel, AllMusicCategory
import datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from khafre.utils.json_response import json_resp
from khafre.utils.pags import api_paging, js_resp_paging
from django.views.generic import DetailView
from django.core.cache import caches
from django.db.models import Q
from khufu.version import Version_check
from .cache_manager import update_hour_click, get_hour_click
from khafre.tasks import praise_msg, comment_msg
from khafre.main.cache_manager import up_notifactions_count, up_all_click_count, up_all_share_count, \
    get_all_share_count, read_from_cache, get_all_click_count, write_to_cache
from relationships import Relationship
from khafre.utils.praiseship import Praiseship
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from khufu.settings import redis_ship, chorusplay_url
from khafre.utils.language import check_lan
# from khafre.utils.language import check_lan
# lan_code=check_lan(request)

p = Praiseship()
r = Relationship(redis_ship)
# 缓存

cache_count = caches['count']
cache_hour = caches['hour_count']


# @receiver(post_save, sender=ALLComment)
# def my_handler(sender, instance, created, **kwargs):
#     to_user = instance.music.all_music_auth
#     from_user = instance.user
#     post_id = instance.music.id
#     title = 'new comment'
#     text = 'comment your post'
#     type = 'comment'
#     link = "http://127.0.0.1:8000/api/v1/music/allmusicdetail/{0}/".format(post_id)
#     add = NotificationApp.objects.create(title=title, text=text, link=link, from_user=from_user, to_user=to_user,
#                                          type=type)
#
#     followers = r(instance.user.id).followers()  # 粉丝
#     to_user_id = instance.music.all_music_auth.id
#     if str(to_user_id) in followers:
#         followers.remove(str(to_user_id))
#
#     to_list = list(followers)
#     for u in to_list:
#         follow_user = User.objects.get(id=u)
#
#         FollowerNotification.objects.create(title='new comment', text='comment', from_user=from_user,
#                                             to_user=follow_user, action_user=to_user, post=post_id, type='comment')
#         up_notifactions_count(u)

#
# @receiver(post_save, sender=ALLMusicPraise, dispatch_uid='ALLMusicPraise_created_save')
# def my_handler1(sender, instance, **kwargs):
#     to_user = instance.music.all_music_auth
#     from_user = instance.owner
#     post_id = instance.music.id
#     title = 'new praise'
#     text = 'praise your post'
#     type = 'praise'
#     link = "http://127.0.0.1:8000/api/v1/music/allmusicdetail/{0}/".format(post_id)
#     NotificationApp.objects.create(title=title, text=text, link=link, from_user=from_user, to_user=to_user,
#                                    post=post_id, type=type)
#
#     followers = r(instance.owner.id).followers()  # 粉丝
#     to_user_id = instance.music.all_music_auth.id
#     if str(to_user_id) in followers:
#         followers.remove(str(to_user_id))
#
#     to_list = list(followers)
#     for u in to_list:
#         follow_user = User.objects.get(id=u)
#
#         FollowerNotification.objects.create(title='new praise', text='praise', from_user=from_user,
#                                             to_user=follow_user, action_user=to_user, post=post_id, type='praise')
#         up_notifactions_count(u)


class My_Post_View(APIView):
    """
    OK 
    2018/2/27
    我发布的视频
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        all_post = AllSongMusic.objects.filter(all_music_auth=user.id, is_delete=False).order_by('-created_at')

        return js_resp_paging(all_post, request, AllSongMusic_Popular_Serializer)


class Whos_Post_View(APIView):
    """
    OK
    2018/2/27
    查看某人的视频
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        code_lag=check_lan(request)
        try:
            all_post = AllSongMusic.objects.filter(all_music_auth=pk, is_enable=True, is_delete=False)
            return js_resp_paging(all_post, request, AllSongMusic_Popular_Serializer)
        except User.DoesNotExist:
            return json_resp(code=499, msg=code_lag['499'])


class PopularView(APIView):
    """
    OK
    code
    populer首页视图
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_music = AllSongMusic.objects.filter(Q(rank__gt=0), is_delete=False, is_enable=True).order_by('-rank')
        return js_resp_paging(all_music, request, AllSongMusic_Popular_Serializer)


class AllMusicDetail(APIView):
    """
    ok
    2018/2/27
    code
    417:not vedio
    查案合唱视频
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return AllSongMusic.objects.get(pk=pk)
        except AllSongMusic.DoesNotExist:
            return None

    def get(self, request, pk):
        code_lag=check_lan(request)
        up_all_click_count(pk)
        # update_hour_click(pk, "allmusic")
        redis_db = read_from_cache(pk, 'allmusic')
        music = self.get_object(pk)
        if music:
            pass
        else:
            return json_resp(code=479,msg=code_lag['479'])
        owner_id = request.user.id
        if p(owner_id).is_loveing(pk):
            is_praise = True
        else:
            is_praise = False
        share_count = get_all_share_count(pk)
        praise_redis_count = p(pk).lovedby_count()

        praise_count=music.praise+praise_redis_count
        click_count = get_all_click_count(pk)
        comment_count = music.all_music_comment.count()

        if redis_db:
            redis_db["is_praise"] = is_praise
            redis_db['share_count'] = share_count
            redis_db['praise_count'] = praise_count
            redis_db['view_count'] = click_count
            redis_db['comment_count'] = comment_count
            return json_resp(code=200, msg='ok',
                             data=redis_db)
        else:

            if music:
                if music.is_delete:
                    return json_resp(code=479, msg=code_lag['479'])
                else:

                    serializer = AllSongMusicDetailSerializer(music)

                    data = serializer.data
                    data['is_praise'] = is_praise
                    data['share_count'] = share_count
                    data['praise_count'] = praise_count
                    data['view_count'] = click_count
                    data['comment_count'] = comment_count
                    write_to_cache(pk, 'allmusic', data)
                    return json_resp(code=200, msg='ok', data=data)
            else:
                return json_resp(code=479, msg=code_lag['479'])


class Musci_praise_View(APIView):
    """
    OK
    2018/2/27
    code
    418:un praise ok
    419:praise ok
    点赞视频

    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return AllSongMusic.objects.get(pk=pk)
        except AllSongMusic.DoesNotExist:
            return None

    def put(self, request, pk):
        code_lag=check_lan(request)

        music = self.get_object(pk)
        if not music:
            return json_resp(code=479, msg=code_lag['479'])
        else:

            owner_id = request.user.id

            if p(owner_id).is_loveing(pk):
                p(owner_id).unpraise(pk)
                return json_resp(code=200, msg=code_lag['200'])

            else:
                p(owner_id).praise(pk)
                to_user_id = music.all_music_auth.id
                from_user = owner_id

                praise_msg.delay(from_user, to_user_id, music.id)
                return json_resp(code=200, msg=code_lag['200'])


class Music_comment_View(APIView):
    """
    OK
    2018/2/27
    GET查看视频评论
    POST对视频进行评论
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return AllSongMusic.objects.get(pk=pk)
        except AllSongMusic.DoesNotExist:
            return None

    def get(self, request, pk):
        comment = ALLComment.objects.select_related().filter(music=pk)
        return js_resp_paging(comment, request, All_comment_serializer, pages=20)

    def post(self, request, pk):
        code_lag=check_lan(request)
        music = self.get_object(pk)
        user = request.user
        data = request.data
        data['user'] = user.id
        data['music'] = pk
        if music:
            to_user = music.all_music_auth
        else:
            return json_resp(code=479, msg=code_lag['479'])

        serializer = ALLCommentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user, music=music)
            # up_notifactions_count(music.all_music_auth.id)
            comment_msg(request.user.id, to_user.id, music.id)
            return json_resp(code=200, msg="ok")
        else:
            return json_resp(code=484, msg=code_lag['484'])


class Del_Music_View(APIView):
    """
    OK
    2018/2/27
    删除自己的视频

    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return AllSongMusic.objects.get(pk=pk)
        except AllSongMusic.DoesNotExist:
            return None

    def put(self, request, pk):
        code_lag = check_lan(request)
        music = self.get_object(pk)
        if music:
            auth = music.all_music_auth
            if request.user == auth:
                data_copy = request.data.copy()
                data_copy['is_delete'] = True
                data_copy['deleted_at'] = datetime.datetime.now()
                serializer = CreateAllSongMusicSerializer(music, data=data_copy, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return json_resp(code=200, msg='ok')
                return json_resp(code=499, msg=code_lag['499'])
            else:
                return json_resp(code=480, msg=code_lag['480'])
        else:
            return json_resp(code=479, msg=code_lag['479'])


class H5Music(DetailView):
    """
    OK
    视频浏览网页页面

    """
    context_object_name = "music_list"
    model = AllSongMusic
    template_name = 'include/vedioplay/indexvdeio.html'

    def get_context_data(self, **kwargs):
        context = super(H5Music, self).get_context_data(**kwargs)
        if context:
            is_enable = context['music_list'].is_enable
            if is_enable:
                context['now'] = datetime.datetime.now()
                click_count = get_hour_click(self.kwargs['pk'], 'allmusic')
                hour_click = update_hour_click(self.kwargs['pk'], 'allmusic')
                return context
            else:
                context = None
        else:
            return None


def H5shareMusict(request, pk):
    """
    OK
    2018/2/27
    分享HTML页面
    :param request: 
    :param pk: 
    :return: 
    """

    try:
        recommend = AllSongMusic.objects.select_related().filter(is_delete=0, is_enable=1)[6]
    except:
        recommend = AllSongMusic.objects.select_related().filter(is_delete=0, is_enable=1)

    obj_list = []
    for r in recommend:
        obj_di = {}
        music_id = r.id
        if r.share_jpg_key:
            photo_key = r.share_jpg_key
            photo_url = chorusplay_url + "out_jpg/" + photo_key
        else:
            photo_url = chorusplay_url + "out_jpg/default.jpg"

        obj_di['id'] = music_id
        obj_di['photo'] = photo_url
        obj_list.append(obj_di)

    response = render_to_response('include/share.html', {
        "recommend": obj_list}, context_instance=RequestContext(request))

    response['Access-Control-Allow-Origin'] = '*'
    return response


class H5shareMusic(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return AllSongMusic.objects.get(pk=pk)
        except AllSongMusic.DoesNotExist:
            return None

    def get(self, request, pk):
        code_lag = check_lan(request)
        music = self.get_object(pk)
        if music:
            ser_data = AllSongMusic_html5_Serializer(music)

            data = ser_data.data

            return json_resp(code=200, msg='ok', data=data)
        else:
            return json_resp(code=479, msg=code_lag['479'])


class SearchSingerSongView(APIView):
    """
    2018/2/27
    OK
    搜索歌手/歌曲名、用户
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset_singer(self, word):
        queryset_singer = Singer.objects.filter(Q(singer_name__istartswith=word)).order_by('-rank')

        if word:
            return queryset_singer
        else:
            return None

    # def get_queryset_song(self, word):
    #     queryset_song = AllSongMusic.objects.filter(
    #         Q(music_info__singer__singer_name__icontains=word) | Q(music_info__music_name__icontains=word),
    #         is_enable=True, is_delete=False).order_by('-rank', '-view_count', '-created_at')
    #     return queryset_song

    def get_queryset_users(self, word):
        queryset_user = User.objects.filter(Q(username__istartswith=word))

        if word:
            return queryset_user
        else:
            return None

    def get_queryset_music(self, word):
        queryset_music = MusicProfiel.objects.filter(
            Q(singer__singer_name__icontains=word) | Q(music_name__icontains=word), is_online=True).order_by(
            "-rank").distinct()
        return queryset_music

    def post(self, request):
        code_lag = check_lan(request)
        slug = self.request.data.get('slug', '')
        word = self.request.data.get('word', "")
        if word:
            if slug == 'song':
                music = self.get_queryset_music(word)
                singer = self.get_queryset_singer(word=word)
                if singer:
                    type = 0
                else:
                    type = 1
                return api_paging(singer=singer, song=music, Serializer_singer=SingerSerializer,
                                  Serializer_song=MusicProfileSearchSer, request=request, type=type, return_count=10)
            elif slug == 'people':
                users = self.get_queryset_users(word=word)
                return js_resp_paging(objs=users, request=request, serializer_obj=AccountSerializer, pages=20)
            else:
                return json_resp(code=499, msg=code_lag['499'])
        else:
            return json_resp(code=486, msg=code_lag['486'])


class SearchPostView(APIView):
    """
    OK

    2018/2/27
    点击搜索结果
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, slug):
        if slug == "singer":
            all_post = AllSongMusic.objects.filter(music_info__singer__id=pk, is_enable=True, is_delete=False)
        else:
            # user = User.objects.get(id=pk)
            all_post = AllSongMusic.objects.filter(music_info_id=pk, is_enable=True, is_delete=False)
        return js_resp_paging(all_post, request, AllSongMusicSearchSerializer)


class Recommend_Vedio_View(APIView):
    """
        OK
        2018/2/27
        推荐给新用户的视频is_recommend_rank
        """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_post = AllSongMusic.objects.filter(is_enable=True, is_delete=False).order_by('-is_recommend_rank')

        return js_resp_paging(all_post, request, AllSongMusicRecommendSerializer, pages=10)


class All_Category_View(APIView):
    """
            OK
            2018/2/27
            搜索页面模块，下面有个分类显示作品，此接口显示所有的分类作品
        """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_category = AllMusicCategory.objects.select_related().filter(is_online=True)

        return js_resp_paging(all_category, request, All_Category_Serializer, pages=20)
