#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/3/30 下午5:06
@SOFTWARE:PyCharm
"""

from khafre.main.serilizers import AllSongMusicSearchSerializer, ReportSongSerializer, \
    MusicProfileSingerSerializer, CreatePartSongSerializer, CreateAllSongMusicSerializer, PartRandomSerializer
from dao.models.music import Singer, MusicProfiel, PartSongMusic, PartComment, AllSongMusic, ALLComment, \
    ALLMusicPraise, \
    ReportSong, Notification
from dao.models.base import Banner
from app_auth.models import NotificationApp, User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from khafre.utils.json_response import json_resp, JsonResponse_zj
from khafre.utils.pags import api_paging, js_resp_paging, js_resp_sing_paging

from django.views.generic import View
from django.core.cache import caches
from django.db.models import Q
from khufu import settings
from .serializers import BannerSerializer
from khafre.main.serilizers import MusicProfileSearchSer
import os, sys, random, time, re
from relationships import Relationship
import json
from khafre.tasks import music_lambda, con_linux, up_to_aws
from django.http.request import QueryDict
from fcm_django.models import FCMDevice
from khafre.main.cache_manager import up_notifactions_count
from dao.models.base import PostData
import base64
from app_auth.models import MobileVersion
from khufu.settings import onegif_url, onejpg_url, allgif_url, partplay_url, chorusplay_url, musicimg_url, userpic_url
import time, datetime
import logzero, logging
from khafre.utils.language import check_lan

logger_in = logzero.setup_logger(name="mylogger", logfile="/tmp/test-logger.log", level=logging.ERROR)

# 缓存
try:
    cache = caches['mencache']
except ImportError as e:
    cache = caches['default']

from khufu.settings import redis_ship

r = Relationship(redis_ship)


# def my_handler(sender, instance, **kwargs):
#     to_user = instance.all_music_auth
#     from_user = instance.all_music_auth
#     title = 'new post'
#     text = 'post a sing'
#     type = 'post'
#
#     add = NotificationApp.objects.create(title=title, text=text, from_user=from_user, to_user=to_user, type=type)
#


def up_file_cut(request, file, banzou_path, lyr_time):
    """上传MP4分解返回音频和视频"""
    # file_name = ""
    #
    # try:
    #     path = "media/image" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #         file_name = path + f.name
    #         destination = open(file_name, 'wb+')
    #         for chunk in f.chunks():
    #             destination.write(chunk)
    #         destination.close()
    # except Exception, e:
    #     print e
    #
    # return file_name

    up_file = file
    fn = time.strftime('%Y%m%d%H%M%S')

    user_name = request.user.username
    up_file_name = 'mp4_up' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    out_vedio_name = 'mp4_out' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    out_aac_name = 'aac_out' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    ocompose_aac_name = 'aac_compose' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    compose_vedio_name = 'mp4_compose' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    out_jpg_name = 'jpg_out' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.jpg'

    try:

        f = open(os.path.join('media/music', up_file_name), 'wb')
        for chunk in up_file.chunks():
            f.write(chunk)

            # up_file_path = os.path.join('/media/music', up_file_name)


    except Exception as e:

        return ""
    f.close()

    # filedir = os.path.join(os.path.dirname(settings.__file__), 'media/music/')
    filedir = os.path.dirname(os.path.dirname(settings.__file__)) + '/media/music/'

    out_aac_path = filedir + out_aac_name
    up_file_path = filedir + up_file_name
    out_vedio_path = filedir + out_vedio_name
    banzou_dir_path = os.path.dirname(os.path.dirname(settings.__file__)) + '/' + banzou_path
    ocompose_aac_path = filedir + ocompose_aac_name
    compose_vedio_path = filedir + compose_vedio_name
    out_jpg_path = filedir + out_jpg_name
    # if up_file_path:
    path_data = {}
    try:
        # os.system(
        #     "/usr/local/bin/ffmpeg -i %s -vn -y -acodec aac -ab 128k -ar 44100 -ac 1 %s" % (up_file_path,
        # out_aac_path))
        # os.system("/usr/local/bin/ffmpeg -i %s -an -y -strict -2 -vf scale=320:360,crop=320:360:20:4 -r 15 -b 99k
        # %s" % (
        #     up_file_path, out_vedio_path))
        # os.system(
        #     "/usr/local/bin/ffmpeg -i %s -i %s -filter_complex amix=inputs=2:duration=longest:dropout_transition=2
        #  -ab 128k -ar 44100 -ac 1 %s" % (
        #         out_aac_path, banzou_dir_path, ocompose_aac_path))
        # os.system("/usr/local/bin/ffmpeg -i %s -i %s -vcodec copy -acodec copy %s" % (
        # out_vedio_path, ocompose_aac_path, compose_vedio_path))
        # os.system("/usr/local/bin/ffmpeg -i %s -y -f image2 -ss 8 -t 0.001 -s 320x360 %s" % (
        # compose_vedio_path, out_jpg_path))

        # 裁剪视频得到裁剪的视频加干声MP4
        os.system(
            "/usr/local/bin/ffmpeg -i %s -strict -2 -vf scale=320:360,crop=320:360:20:4 -r 15 -b 150k -ab 128k -ar "
            "44100 -ac 1 %s" % (
                up_file_path, out_vedio_path))

        # 将裁剪得到的视频加入伴奏得到完成的MP4视频
        os.system("/usr/local/bin/ffmpeg -i %s -i %s -vcodec copy -acodec copy %s" % (
            out_vedio_path, banzou_dir_path, compose_vedio_path))

        # 将合成的视频截取图片
        os.system("/usr/local/bin/ffmpeg -i %s -y -f image2 -ss %d -t 0.001 -s 320x360 %s" % (
            compose_vedio_path, lyr_time, out_jpg_path))

        path_data = {'out_vedio_name': out_vedio_name,
                     'compose_vedio_name': compose_vedio_name, 'out_jpg_name': out_jpg_name}
        return path_data
    except Exception as e:
        return e


def up_file(request, my_file):
    """
    :param request: request
    :param up_file: 上传文件
    :return: ret['data':文件路径,
                'error':错误信息]

    上传文件函数
    上传一个文件，文件命名为:上传文件后缀_用户名_当前时间戳_5为随机数
    返回文件所在相对位置"media/music/(file_name)"
    """
    ret = {'error': '', "data": ""}
    try:

        fn = time.strftime('%Y%m%d%H%M%S')
        user_name = request.user.username
        file_name_last = str(my_file.name).split('.')[-1]
        file_name_first = file_name_last + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999)
        file_name = "%s.%s" % (file_name_first, file_name_last)
        f = open(os.path.join('media/music', file_name), 'wb')
        for chunk in my_file.chunks(chunk_size=1024):
            f.write(chunk)
        file_path = os.path.join('/media/music', file_name)
        sys_path = os.path.dirname(os.path.dirname(settings.__file__))
        path = sys_path + file_path
        if os.path.exists(path):
            ret["data"] = file_path
        else:
            ret["error"] = 'not find file'
        f.close()
        return ret
    except Exception as e:
        ret['error'] = e
        return ret


def dispose_part_ffmpeg(request, part_file, banzou_file, lyr_time):
    """
    处理part部分上传后的MP4进行裁剪，合成，取图
    :param request: 
    :param part_file: 文件的路径
    :param banzou_file: 伴奏文件路径
    :param lyc_time: 歌词开始唱歌的时间点向前一秒(int)永远截取视屏某个时间点（秒）的图片
    :return: 
    """
    ret = {"error": '', "data": ''}

    fn = time.strftime('%Y%m%d%H%M%S')
    user_name = request.user.username

    out_vedio_name = 'mp4_out' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    compose_vedio_name = 'mp4_compose' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    out_jpg_name = 'jpg_out' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.jpg'

    filedir = os.path.dirname(os.path.dirname(settings.__file__)) + '/media/music/'
    file_path = os.path.dirname(os.path.dirname(settings.__file__)) + '/' + part_file
    banzou_path = os.path.dirname(os.path.dirname(settings.__file__)) + '/' + banzou_file

    out_vedio_path = filedir + out_vedio_name
    compose_vedio_path = filedir + compose_vedio_name
    out_jpg_path = filedir + out_jpg_name

    try:
        # 裁剪视频得到裁剪的视频加干声MP4
        os.system(
            "/usr/local/bin/ffmpeg -i %s -strict -2 -vf scale=320:360,crop=320:360:20:4 -r 15 -b 150k -ab 128k -ar "
            "44100 -ac 1 %s" % (
                file_path, out_vedio_path))
        if not os.path.exists(out_vedio_path):
            ret['error'] = 'not out_vedio_path'
            return ret
        # 将裁剪得到的视频加入伴奏得到完成的MP4视频
        os.system("/usr/local/bin/ffmpeg -i %s -i %s -vcodec copy -acodec copy %s" % (
            out_vedio_path, banzou_path, compose_vedio_path))

        if not os.path.exists(compose_vedio_path):
            ret['error'] = 'not compose_vedio_path'
            return ret
        # 将合成的视频截取图片

        os.system("/usr/local/bin/ffmpeg -i %s -y -f image2 -ss %d -t 0.001 -s 320x360 %s" % (
            compose_vedio_path, lyr_time, out_jpg_path))

        if not os.path.exists(out_jpg_path):
            ret['error'] = 'not out_jpg_path'
            return ret
        ret_path = 'media/music/'

        path_data = {'out_vedio_path': ret_path + out_vedio_name,
                     'compose_vedio_path': ret_path + compose_vedio_name, 'out_jpg_path': ret_path + out_jpg_name}
        ret['data'] = path_data
        return ret
    except Exception as e:
        ret["error"] = e
        return ret


def dispose_all_ffmpeg(event, context):
    """
    处理allmusic部分合成视频左右拼接合成，截取图片
    :param request: 
    :param auth_vedio: auth部分的MP4（伴奏+干声+视频）
    :param participant_video: 参与者(我)部分MP4（干声+视频）
    :param lyc_time: 取图时间点
    :return: 
    """
    import urllib
    import oss2
    json_string = json.dumps(event)
    evt = json.loads(json_string)

    fn = time.strftime('%Y%m%d%H%M%S')
    user_name = evt['username']
    my_post_url = evt['my_mp4_url']
    part_music_url = evt['part_music_url']
    banzou_url = evt['banzou']
    # participant_post_url=evt["participant_vedio"]
    # part_to=evt["patr_to"]
    # 下载我的歌曲MP4
    filedir = '/tmp/'
    my_post_url_list = my_post_url.split('/')
    my_file_path = filedir + my_post_url_list[-1]

    # urllib.urlretrieve(my_post_url, my_file_path)

    # 下载伴奏
    banzouurl_list = banzou_url.split('/')
    banzoufile_path = '/tmp/' + banzouurl_list[-1]
    # urllib.urlretrieve(banzou_url, banzoufile_path)

    # 下载对方歌曲MP4
    part_music_list = part_music_url.split('/')
    part_file_path = filedir + part_music_list[-1]

    # urllib.urlretrieve(part_music_url, part_file_path)

    out_vedio_name = 'mp4_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    out_aac_name = 'aac_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    out_voice_name = 'voice_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    out_media_name = 'media_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    part_music_vedio_name = 'part_music_mp4' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000,
                                                                                                   99999) + '.mp4'
    out_part_jpg_name = 'jpg_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.jpg'

    all_music_video_name = 'allmusic_mp4_' + user_name + '_' + fn + '_%d' % random.randint(10000,
                                                                                           99999) + '.mp4'
    out_all_jpg_name = 'allmusic_jpg_' + user_name + '_' + fn + '_%d' % random.randint(10000,
                                                                                       99999) + '.jpg'

    out_vedio_path = filedir + out_vedio_name  # 裁剪后视频
    out_aac_path = filedir + out_aac_name  # 视频取出的音频
    out_voice_path = filedir + out_voice_name  # 音频和伴奏的合成
    out_media_path = filedir + out_media_name  # 视频取出的视频无声音
    part_music_vedio_path = filedir + part_music_vedio_name  # 合成后的视频
    out_part_jpg = filedir + out_part_jpg_name  # 截图

    all_music_video_path = filedir + all_music_video_name  # 合唱合成视频
    out_all_jpg_path = filedir + out_all_jpg_name  # 合唱合成图片

    try:
        # part部分合成好的视屏+刚刚拍摄剪切的视频合成新的视频
        # part = int(part_to)

        # 裁剪视频得到裁剪的视频加干声MP4

        os.system(
            "/usr/local/bin/ffmpeg -i %s -strict -2 -vf scale=320:360,crop=320:360:20:4 -ac 2 %s" % (
                my_file_path, out_vedio_path))
        print "out_vedio_path:%s" % out_vedio_path
        # 取音频
        os.system("/usr/local/bin/ffmpeg -i %s -vn -ac 2 %s" % (
            out_vedio_path, out_aac_path))
        print "out_aac_path:%s" % out_aac_path
        # 取视频
        os.system("/usr/local/bin/ffmpeg -i %s -an %s" % (
            out_vedio_path, out_media_path))
        print "out_media_path:%s" % out_media_path

        # 音频伴奏合成
        os.system(
            "/usr/local/bin/ffmpeg -i %s -i %s -filter_complex amix=inputs=2:duration=longest:dropout_transition=2 "
            "-ac 2 %s" % (
                out_aac_path, banzoufile_path, out_voice_path))
        print "out_voice_path:%s" % out_voice_path

        # 音频视频合成
        os.system(
            "/usr/local/bin/ffmpeg -i %s -i %s -ac 2 %s" % (
                out_media_path, out_voice_path, part_music_vedio_path))
        print "part_music_vedio_path:%s" % part_music_vedio_path

        # 截图
        os.system("/usr/local/bin/ffmpeg -i %s -y -f image2 -ss 8 -t 0.001 -s 320x360 %s" % (
            part_music_vedio_path, out_part_jpg))
        print "out_part_jpg:%s" % out_part_jpg

        # 合成视频左边永远是发布者


        os.system(
            "/usr/local/bin/ffmpeg -i %s -i %s -filter_complex \"[0:v]pad=w=iw*2:h=ih[b];[b][1:v]overlay=x=W/2\" "
            "-filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -ac 2 %s" % (
                part_music_vedio_path, part_file_path, all_music_video_path))
        print "start all"
        print "all_music_video_path:%s" % all_music_video_path

        # elif part == 0:
        #     os.system(
        #         "/usr/local/bin/ffmpeg -i %s -i %s -filter_complex \"[0:v]pad=w=iw*2:h=ih[b];[b][
        # 1:v]overlay=x=W/2\" -filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -ab 128k -ar
        #  44100 -ac 1 -r 15 -b 150k %s" % (
        #             music_participant_part_vedio_path, music_auth_part_vedio_path, compose_video_path))
        # 对新合成视频截图
        os.system("/usr/local/bin/ffmpeg -i %s -y -f image2 -ss 8 -t 0.001 -s 640x360 %s" % (
            all_music_video_path, out_all_jpg_path))
        print "out_all_jpg_path:%s" % out_all_jpg_path

        try:
            auth = oss2.Auth('LTAIXeFWeGVCQS3r', 'NNgpxxKyIfAr4J9RJ4N4AHlYvX7a9e')
            print "shangchuan part"
            bucket_part = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'duetin-part')
            with open(part_music_vedio_path, 'rb') as filepart_v:
                bucket_part.put_object('compose_vedio/' + part_music_vedio_name, filepart_v)

            with open(out_part_jpg, 'rb') as filepart_j:
                bucket_part.put_object('out_jpg/' + out_part_jpg_name, filepart_j)

            part_music_mp4_path = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/compose_vedio/' + \
                                  part_music_vedio_name
            part_music_jpg_path = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/out_jpg/' + out_part_jpg_name

            print "shangchuan all"

            bucket_all = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'duetin-all')
            with open(all_music_video_path, 'rb') as file_all_v:
                bucket_all.put_object('compose_vedio/' + all_music_video_name, file_all_v)

            with open(out_all_jpg_path, 'rb') as fileobj:
                bucket_all.put_object('out_jpg/' + out_all_jpg_name, fileobj)

            all_music_mp4_path = 'http://duetin-all.oss-cn-shanghai.aliyuncs.com/compose_vedio/compose_vedio/' + \
                                 all_music_video_name
            all_music_jpg_path = 'http://duetin-all.oss-cn-shanghai.aliyuncs.com/compose_vedio/out_jpg/' + \
                                 out_all_jpg_name

            l = {
                "part_music_mp4_path": part_music_mp4_path,
                "part_music_jpg_path": part_music_jpg_path,
                "all_music_mp4_path": all_music_mp4_path,
                "all_music_jpg_path": all_music_jpg_path
            }

            # os.system('rm  -rf /tmp/*')
            return json.dumps(l)
        except oss2.exceptions.code as e:
            # os.system('rm  -rf /tmp/*')
            data = {"code": 400, "msg": e, "data": ""}

            return json.dumps(data)
    except:
        # os.system('rm  -rf /tmp/*')

        data = {"code": 400, "msg": "ffmpeg error", "data": ""}

        return json.dumps(data)


def dispose_all_ffmpeglam(request, part, auth_vedio, participant_video, lyr_time):
    """
    处理allmusic部分合成视频左右拼接合成，截取图片
    :param request: 
    :param auth_vedio: auth部分的MP4（伴奏+干声+视频）
    :param participant_video: 参与者(我)部分MP4（干声+视频）
    :param lyc_time: 取图时间点
    :return: 
    """
    ret = {"error": '', "data": ''}
    fn = time.strftime('%Y%m%d%H%M%S')

    user_name = request.user.username
    filedir = os.path.dirname(os.path.dirname(settings.__file__)) + '/media/music/'
    compose_video_name = 'allmusic_mp4_' + user_name + '_' + fn + '_%d' % random.randint(10000,
                                                                                         99999) + '.mp4'
    out_jpg_name = 'allmusic_jpg_' + user_name + '_' + fn + '_%d' % random.randint(10000,
                                                                                   99999) + '.jpg'
    music_auth_part_vedio_path = os.path.dirname(os.path.dirname(settings.__file__)) + '/' + auth_vedio
    music_participant_part_vedio_path = os.path.dirname(os.path.dirname(settings.__file__)) + '/' + participant_video
    compose_video_path = filedir + compose_video_name
    out_jpg_path = filedir + out_jpg_name

    try:
        # part部分合成好的视屏+刚刚拍摄剪切的视频合成新的视频
        part = int(part)
        if part == 1:

            os.system(
                "/usr/local/bin/ffmpeg -i %s -i %s -filter_complex \"[0:v]pad=w=iw*2:h=ih[b];[b][1:v]overlay=x=W/2\" "
                "-filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -ab 128k -ar 44100 -ac 1 "
                "-r 15 -b 150k %s" % (
                    music_auth_part_vedio_path, music_participant_part_vedio_path, compose_video_path))
        elif part == 0:
            os.system(
                "/usr/local/bin/ffmpeg -i %s -i %s -filter_complex \"[0:v]pad=w=iw*2:h=ih[b];[b][1:v]overlay=x=W/2\" "
                "-filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -ab 128k -ar 44100 -ac 1 "
                "-r 15 -b 150k %s" % (
                    music_participant_part_vedio_path, music_auth_part_vedio_path, compose_video_path))
        # 对新合成视频截图
        os.system("/usr/local/bin/ffmpeg -i %s -y -f image2 -ss %d -t 0.001 -s 640x360 %s" % (
            compose_video_path, lyr_time, out_jpg_path))

        if os.path.exists(compose_video_path) and os.path.exists(out_jpg_path):

            path_data = {'out_vedio_name': 'media/music/' + compose_video_name,
                         'out_jpg_name': 'media/music/' + out_jpg_name}
            ret['data'] = path_data
            return ret
        else:
            return json_resp(code=400, msg="error")


    except Exception as e:
        ret['error'] = e
        return ret


class BannerView(APIView):
    """
    OK
    2018/2/28
    BANNER

    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return Banner.objects.filter(is_delete=False).order_by('-rank')
        except Banner.DoesNotExist:
            return None

    def get(self, request):
        banner = self.get_object()
        if banner:
            return js_resp_paging(banner, request, BannerSerializer)
        else:
            return json_resp(code=499, msg='not this music')


class SingIndexView(APIView):
    """
    OK
    2018/2/28
    唱歌主页面pop/new
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return MusicProfiel.objects.filter(is_delete=False, is_online=True)

    def get(self, request, slug):
        if slug == 'new':
            music_pro = self.get_object().filter(~Q(new_sort=0)).order_by('-new_sort', '-created_at', '-view_count')

        elif slug == 'pop':
            music_pro = self.get_object().order_by('-sort', '-rank', '-view_count')
        else:
            music_pro = None

        return js_resp_paging(music_pro, request, MusicProfileSingerSerializer, pages=10)


# top50手动排序
class TopSortView(APIView):
    """
    OK
    2018/2/28
    手动排序前50
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):

        return MusicProfiel.objects.filter(is_delete=False, is_online=True).order_by("-top_rank")[:50]

    def get(self, request):
        code_lag = check_lan(request)
        music_pro = self.get_object()

        if music_pro:
            return js_resp_paging(music_pro, request, MusicProfileSingerSerializer, pages=10)
        else:
            return json_resp(code=483, msg=code_lag['483'])


class Search_sing(APIView):
    """
    OK
    2018/2/28
    唱歌页面搜索歌曲
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, word):
        data = MusicProfiel.objects.filter(
            Q(singer__singer_name__istartswith=word) | Q(music_name__icontains=word)).distinct().order_by('-is_online',
                                                                                                          '-rank')
        return data

    def post(self, request):
        code_lag = check_lan(request)
        word = self.request.data.get('word', '')
        if word:

            data = self.get_queryset(word)
        else:
            return json_resp(code=486, msg=code_lag['486'])

        if data:
            return js_resp_paging(objs=data, request=request, serializer_obj=MusicProfileSingerSerializer, pages=10)
        else:
            return json_resp(code=486, msg=code_lag['486'])


class SingView(APIView):
    """
    待优化
    OK
    code
    422: music not online

    点击唱歌
    请求方法GET  url参数PK:歌曲表ID ，若返回数据result中含有is_loved=True,则这首歌为男女对唱歌曲，需要用户选择进入哪一个部分，0标识男，1标识女。
                用户选择之后，PUT方法，带参数part（0和1标识男女部分），
                 返回：若为第一个唱歌者返回musicinfo表 ，若合唱返回partmusicsong表信息，resule中包含participant_part信息：
                 is_first：为Ture，则第一个唱，false为加入合唱，part代表加入的部分
    PUT：当歌曲为男女对唱时候，需要用户选择那一部分之后，带上part参数重新获取歌曲信息
        返回信息与get非男女对唱歌曲一样的信息

    POST  URL参数PK：音乐信息ID  所需参数：title：标题（str），socre:得分（int），part:合唱歌曲的哪个部分(若A部分0，B部分1，即为GET到的PART数据），
                                    is_enable:是否公开（bool，True或者False）,vedio:录制的视频MP4文件


    """
    permission_classes = (IsAuthenticated,)
    from khufu.version import Version_check
    versioning_class = Version_check

    def get_music_info(self, pk):
        try:
            music_info = MusicProfiel.objects.get(pk=pk)
            return music_info
        except:
            return None
            # music_info.view_count += 1
            # music_info.save()

    def get_object(self, pk, delay_time, error_count):

        """
        返回数据：
        "is_loved": 是否男女对唱,
        "participant_user_name": 合唱者用户名, 
        "participant_user_picture": 合唱者头像,
        "lyrics": 歌词地址, 
        "banzou_url": 伴奏地址（MP4), 
        "part_music_id": 合唱part部分id,
        'part_to': 用户要唱的部分,
        "my_user_id":当前登录账户id,
        'is_first': 是否第一次唱,
        "music_id":歌曲ID

        :param pk: 
        :param request: 
        :return: 
        """
        code_lag = check_lan(self.request)
        music_data = self.get_music_info(pk=pk)
        if not music_data:
            return json_resp(code=420, msg='no data')
        else:
            music_info = music_data

        if music_info:
            if music_info.is_online == True:
                part_A_count = music_info.music_part.filter(~Q(rating_scale=5), part=0, is_delete=False,
                                                            is_enable=True).count()
                part_B_count = music_info.music_part.filter(~Q(rating_scale=5), part=1, is_delete=False,
                                                            is_enable=True).count()
                is_loved = music_info.is_loved

                if part_A_count < part_B_count:
                    part_to = 0  # 分配给用户的PART
                    part_from = 1  # 获取伴奏数据的部分
                elif part_A_count == part_B_count:
                    part_list = [0, 1]
                    from random import choice
                    part_to = choice(part_list)
                    if part_to == 0:
                        part_from = 1
                    else:
                        part_from = 0
                else:
                    part_to = 1
                    part_from = 0

                part_music_obj = music_info.music_part.filter(Q(rating_scale__in=[1, 2]), is_delete=False,
                                                              is_enable=True, part=part_from)
                if not part_music_obj:
                    part_music_obj = music_info.music_part.filter(Q(rating_scale=3), is_delete=False,
                                                                  is_enable=True, part=part_from)
                    if not part_music_obj:
                        part_music_obj = music_info.music_part.filter(Q(rating_scale=None), is_delete=False,
                                                                      is_enable=True, part=part_from)
                        if not part_music_obj:
                            part_music_obj = music_info.music_part.filter(Q(rating_scale=4), is_delete=False,
                                                                          is_enable=True, part=part_from)
                part_music = part_music_obj
                if part_music:
                    # my_part = part_music[0]
                    my_part = random.choice(part_music)
                    # serializer = PartSongMusicSerializer(my_part)
                    music_name = music_info.music_name

                    singer = music_info.singer.all()
                    singer_name = []
                    for s in singer:
                        s_n = s.singer_name
                        singer_name.append(s_n)
                    music_image = music_info.image
                    participant_user_name = my_part.music_auth.username  # 合唱者的username
                    participant_user_picture = my_part.music_auth.picture  # 和唱者的头像
                    lyrics_bucket_name = music_info.bucket_lyrics_name  # 歌词
                    lirics_key_name = music_info.bucket_lyrics_key

                    banzou_aac_buctet_name = my_part.hc_aac_bucket_name
                    banzou_aac_key_name = my_part.hc_aac_key_name

                    banzou_mp4_bucket_name = my_part.vedio_bucket_name
                    banzou_mp4_key_name = my_part.vedio_bucket_key

                    # banzou_url = my_part.part_vedio_url # 伴奏（为合唱者生成的MP4）


                    part_music_id = my_part.id  # 合唱者部门id
                    is_first = False
                    music_id = music_info.id  # music歌曲库id
                    my_user_id = self.request.user.id  # 当前登录用户ID
                else:
                    music_name = music_info.music_name
                    singer = music_info.singer.all()
                    singer_name = []
                    for s in singer:
                        s_n = s.singer_name
                        singer_name.append(s_n)
                    music_image = music_info.image

                    # serializer = MusicProfielSerializer(music_info)
                    participant_user_name = ""
                    participant_user_picture = ""
                    lyrics_bucket_name = music_info.bucket_lyrics_name  # 歌词
                    lirics_key_name = music_info.bucket_lyrics_key

                    banzou_aac_buctet_name = music_info.bucket_accompany_name
                    banzou_aac_key_name = music_info.bucket_accompany_key

                    banzou_mp4_bucket_name = ""
                    banzou_mp4_key_name = ""
                    # banzou_url = music_info.accompany

                    part_music_id = 0
                    is_first = True

                    music_id = music_info.id
                    my_user_id = self.request.user.id
                data = {"is_loved": is_loved, "music_name": music_name, "singer_name": singer_name,
                        "music_image": music_image, "participant_user_name": participant_user_name,
                        "participant_user_picture": participant_user_picture,
                        "lyrics_bucket_name": lyrics_bucket_name, "lirics_key_name": lirics_key_name,
                        "banzou_aac_buctet_name": banzou_aac_buctet_name,
                        "banzou_aac_key_name": banzou_aac_key_name, "banzou_mp4_bucket_name": banzou_mp4_bucket_name,
                        "banzou_mp4_key_name": banzou_mp4_key_name, "part_music_id": part_music_id,
                        'part_to': part_to, "my_user_id": my_user_id,
                        'is_first': is_first, "music_id": music_id, "delay_time": delay_time,
                        "error_count": error_count}

                return json_resp(code=200, msg='ok',
                                 data=data)
            else:
                return json_resp(code=491, msg=code_lag['491'])

        else:
            return json_resp(code=483, msg=code_lag['483'])

    def click_count(self, music_id):
        if music_id:
            try:
                music = MusicProfiel.objects.get(id=music_id)
                music.view_count += 1
                music.save()
            except:
                return json_resp(code=483, msg='')
        else:
            return json_resp(code=483, msg='')

    def get(self, *args, **kwargs):

        music_pk = kwargs.pop('pk2', None)
        if music_pk:
            self.click_count(music_pk)

            devicename = kwargs.pop('devicename', None)
            if devicename:
                dn = base64.urlsafe_b64decode(str(devicename))
            else:
                dn = None
            model_name = kwargs.pop('model', None)
            if model_name:
                mn = base64.urlsafe_b64decode(str(model_name))
            else:
                mn = None
            manufacturer = kwargs.pop('manufacturer', None)
            if manufacturer:
                mf = base64.urlsafe_b64decode(str(manufacturer))
            else:
                mf = None
            os_name = kwargs.pop('os', None)
            if os_name:
                os_n = base64.urlsafe_b64decode(str(os_name))
            else:
                os_n = None
            mobile_l = MobileVersion.objects.filter(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                    mobile_edition=os_n).first()

            if mobile_l:
                mobile_id = mobile_l
                t_t = mobile_l.delay_time
                error_count = mobile_l.error_count

            else:
                mobile_id = MobileVersion.objects.create(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                         mobile_edition=os_n,
                                                         default_time=300)
                t_t = 0
                error_count = 0
            my_user_id = self.request.user.id
            my_user = User.objects.get(id=my_user_id)
            my_user.mobile = mobile_id
            my_user.save()
        else:
            music_pk = kwargs.pop('pk1', None)
            self.click_count(music_pk)

            t_t = 0
            error_count = 0
        return self.get_object(pk=music_pk, delay_time=t_t, error_count=error_count)

    def put(self, *args, **kwargs):
        """若为男女对唱歌曲则put重新获取数据"""
        code_lag = check_lan(self.request)
        music_pk = kwargs.pop('pk2', None)
        if music_pk:
            devicename = kwargs.pop('devicename', None)
            if devicename:
                dn = base64.urlsafe_b64decode(str(devicename))
            else:
                dn = None
            model_name = kwargs.pop('model', None)
            if model_name:
                mn = base64.urlsafe_b64decode(str(model_name))
            else:
                mn = None
            manufacturer = kwargs.pop('manufacturer', None)
            if manufacturer:
                mf = base64.urlsafe_b64decode(str(manufacturer))
            else:
                mf = None
            os_name = kwargs.pop('os', None)
            if os_name:
                os_n = base64.urlsafe_b64decode(str(os_name))
            else:
                os_n = None
            mobile_l = MobileVersion.objects.filter(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                    mobile_edition=os_n).first()
            if mobile_l:
                error_count = mobile_l.error_count

                mobile_id = mobile_l
                t_t = mobile_l.delay_time


            else:
                mobile_id = MobileVersion.objects.create(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                         mobile_edition=os_n,
                                                         default_time=300)
                t_t = 0
                error_count = 0

            my_user_id = self.request.user.id
            my_user = User.objects.get(id=my_user_id)
            my_user.mobile = mobile_id
            my_user.save()
        else:
            music_pk = kwargs.pop('pk1', None)

            t_t = 0
            error_count = 0

        part = self.request.data.get('part', None)

        if part:
            part = int(part)
            if part == 1:
                part_to = 1
                part_from = 0
            else:
                part_to = 0
                part_from = 1

            music_data = self.get_music_info(pk=music_pk)
            music_info = music_data
            if music_info:
                singer = music_info.singer.all()
                singer_name = []
                for s in singer:
                    s_n = s.singer_name
                    singer_name.append(s_n)
                music_image = music_info.image
                music_name = music_info.music_name

                if music_info.is_online == True:
                    # part_music = music_info.music_part.filter(is_delete=False, is_enable=True,
                    # part=part_from).order_by(
                    #     "-created_at")
                    part_music_obj = music_info.music_part.filter(Q(rating_scale__in=[1, 2]), is_delete=False,
                                                                  is_enable=True, part=part_from)
                    if not part_music_obj:
                        part_music_obj = music_info.music_part.filter(Q(rating_scale=3), is_delete=False,
                                                                      is_enable=True, part=part_from)
                        if not part_music_obj:
                            part_music_obj = music_info.music_part.filter(Q(rating_scale=None), is_delete=False,
                                                                          is_enable=True, part=part_from)
                            if not part_music_obj:
                                part_music_obj = music_info.music_part.filter(Q(rating_scale=4), is_delete=False,
                                                                              is_enable=True, part=part_from)
                    part_music = part_music_obj
                    if part_music:

                        # my_part = choice(part_music)
                        my_part = random.choice(part_music)
                        # serializer = PartSongMusicSerializer(my_part)
                        # my_part = part_music[0]
                        participant_user_name = my_part.music_auth.username  # 合唱者的username
                        participant_user_picture = my_part.music_auth.picture  # 和唱者的头像
                        lyrics_bucket_name = music_info.bucket_lyrics_name  # 歌词
                        lirics_key_name = music_info.bucket_lyrics_key
                        # banzou_url = my_part.part_vedio_url  # 伴奏（为合唱者生成的MP4）
                        banzou_aac_buctet_name = my_part.hc_aac_bucket_name
                        banzou_aac_key_name = my_part.hc_aac_key_name

                        banzou_mp4_bucket_name = my_part.vedio_bucket_name
                        banzou_mp4_key_name = my_part.vedio_bucket_key

                        part_music_id = my_part.id  # 合唱者部门id
                        is_first = False
                        music_id = music_info.id  # music歌曲库id
                        my_user_id = self.request.user.id  # 当前登录用户ID


                    else:

                        # serializer = MusicProfielSerializer(music_info)
                        participant_user_name = ""
                        participant_user_picture = ""
                        lyrics_bucket_name = music_info.bucket_lyrics_name  # 歌词
                        lirics_key_name = music_info.bucket_lyrics_key
                        # banzou_url = music_info.accompany
                        banzou_aac_buctet_name = music_info.bucket_accompany_name
                        banzou_aac_key_name = music_info.bucket_accompany_key
                        banzou_mp4_bucket_name = ""
                        banzou_mp4_key_name = ""

                        part_music_id = 0
                        is_first = True
                        music_id = music_info.id
                        my_user_id = self.request.user.id
                    data = {"is_loved": True, "music_name": music_name, "singer_name": singer_name,
                            "music_image": music_image, "participant_user_name": participant_user_name,
                            "participant_user_picture": participant_user_picture,
                            "lyrics_bucket_name": lyrics_bucket_name, "lirics_key_name": lirics_key_name,
                            "banzou_aac_buctet_name": banzou_aac_buctet_name,
                            "banzou_aac_key_name": banzou_aac_key_name,
                            "banzou_mp4_bucket_name": banzou_mp4_bucket_name,
                            "banzou_mp4_key_name": banzou_mp4_key_name, "part_music_id": part_music_id,
                            'part_to': part_to, "my_user_id": my_user_id,
                            'is_first': is_first, "music_id": music_id, "delay_time": t_t, "error_count": error_count}
                    return json_resp(code=200, msg='ok',
                                     data=data)
                else:
                    return json_resp(code=491, msg=code_lag['491'])
            else:
                return json_resp(code=483, msg=code_lag['483'])
        else:
            return json_resp(code=499, msg=code_lag['499'])


class SingjoinView(APIView):
    """
    ok

    直接加入选择加入的部分

    GET：url参数：pk：观看的视频的ID，choice表示点击加入哪个部分左边为0右边为1，左边的part永远为music_participant_part，右边永远为music_auth_part，
                    获取到partmusic部分的数据
    POST：URL参数 PK：观看的视频的ID，part表示点击加入到哪个部分左边为0右边为1，
                        所需参数：title：标题（str可空），socre:得分（int），participant_part:被合唱歌曲part部分ID，GET数据的ID），
                                    is_enable:是否公开（bool，True或者False）,vedio:录制的视频MP4文件

    """
    permission_classes = (IsAuthenticated,)
    from khufu.version import Version_check
    versioning_class = Version_check

    def get_object(self, pk, choice):
        try:
            all_song_music = AllSongMusic.objects.get(pk=pk)
        except:
            return None

        choice = int(choice)
        if choice == 1:

            participant_part = all_song_music.music_auth_part
        else:
            participant_part = all_song_music.music_participant_part

        return participant_part

    def click_count(self, music_id):
        if music_id:
            try:
                music = MusicProfiel.objects.get(id=music_id)
                music.view_count += 1
                music.save()
            except:
                return json_resp(code=400, msg="")
        else:
            return json_resp(code=400, msg="")

    def get(self, *args, **kwargs):
        code_lag = check_lan(self.request)

        music_pk = kwargs.pop('pk2', None)
        if music_pk:
            self.click_count(music_pk)

            choice = kwargs.pop('choice2', None)

            devicename = kwargs.pop('devicename', None)
            if devicename:
                dn = base64.urlsafe_b64decode(str(devicename))
            else:
                dn = None
            model_name = kwargs.pop('model', None)
            if model_name:
                mn = base64.urlsafe_b64decode(str(model_name))
            else:
                mn = None
            manufacturer = kwargs.pop('manufacturer', None)
            if manufacturer:
                mf = base64.urlsafe_b64decode(str(manufacturer))
            else:
                mf = None
            os_name = kwargs.pop('os', None)
            if os_name:
                os_n = base64.urlsafe_b64decode(str(os_name))
            else:
                os_n = None
            mobile_l = MobileVersion.objects.filter(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                    mobile_edition=os_n).first()
            if mobile_l:
                mobile_id = mobile_l
                t_t = mobile_l.delay_time
                error_count = mobile_l.error_count
                if t_t == 0:
                    t_t = 300
            else:
                mobile_id = MobileVersion.objects.create(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                         mobile_edition=os_n,
                                                         default_time=300)
                t_t = 300
                error_count = 0
            my_user_id = self.request.user.id
            my_user = User.objects.get(id=my_user_id)
            my_user.mobile = mobile_id
            my_user.save()
        else:
            music_pk = kwargs.pop('pk1', None)
            choice = kwargs.pop('choice1', None)
            self.click_count(music_pk)
            error_count = 0
            t_t = 300

        participant_part = self.get_object(pk=music_pk, choice=choice)
        if not participant_part:
            return json_resp(code=483, msg=code_lag['483'])
        music_info = participant_part.music_info
        singer = music_info.singer.all()
        singer_name = []
        for s in singer:
            s_n = s.singer_name
            singer_name.append(s_n)

        music_image = music_info.bucket_image_key
        if music_image:
            image_url = musicimg_url + music_image
        else:
            image_url = music_info.image
        music_name = music_info.music_name
        part = participant_part.part
        # serializer = PartSongMusicSerializer(music_info)
        participant_user_name = participant_part.music_auth.username  # 合唱者的username

        if participant_part.music_auth.picture_key_name:

            participant_user_picture = userpic_url + participant_part.music_auth.picture_key_name  # 和唱者的头像
        else:
            participant_user_picture = participant_part.music_auth.picture

        lyrics_bucket_name = music_info.bucket_lyrics_name  # 歌词
        lirics_key_name = music_info.bucket_lyrics_key  # banzou_url = participant_part.vedio_url  # 伴奏（为合唱者生成的MP4）

        banzou_aac_buctet_name = participant_part.hc_aac_bucket_name
        banzou_aac_key_name = participant_part.hc_aac_key_name

        banzou_mp4_bucket_name = participant_part.vedio_bucket_name
        banzou_mp4_key_name = participant_part.vedio_bucket_key

        part_music_id = participant_part.id  # 合唱者部门id

        is_first = False
        music_id = music_info.id  # music歌曲库id

        my_user_id = self.request.user.id  # 当前登录用户ID

        if part == 0:
            part_to = 1
        else:
            part_to = 0
        data = {"participant_user_name": participant_user_name,
                "participant_user_picture": participant_user_picture, "music_name": music_name,
                "singer_name": singer_name, "music_image": image_url,
                "lyrics_bucket_name": lyrics_bucket_name, "lirics_key_name": lirics_key_name,
                "banzou_aac_buctet_name": banzou_aac_buctet_name,
                "banzou_aac_key_name": banzou_aac_key_name,
                "banzou_mp4_bucket_name": banzou_mp4_bucket_name,
                "banzou_mp4_key_name": banzou_mp4_key_name, "part_music_id": part_music_id,
                'part_to': part_to, "my_user_id": my_user_id,
                'is_first': is_first, "music_id": music_id, "delay_time": t_t, "error_count": error_count}
        return json_resp(code=200, msg='ok', data=data)


class Report_View(APIView):
    """
    OK
    2018/2/28
    code
    423:not this music
    举报歌曲错误
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            queryset = MusicProfiel.objects.get(id=pk)
            return queryset
        except:
            return None

    def post(self, request, pk):
        code_lag = check_lan(request)
        report_type = self.request.data.get('type', '')

        report_music = self.get_object(pk)
        if report_music:
            data = self.request.data
            data['report_type'] = report_type
            data['report_music'] = pk
            serializer = ReportSongSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                return json_resp(code=200, msg='ok')
            return json_resp(code=499, msg=code_lag['499'])

        else:
            return json_resp(code=483, msg=code_lag['483'])


class post_callback(APIView):
    """
    OK
    2018/2/28

    上传完成 回调数据
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        invite_li = []
        user_id = request.user.id
        username = request.user.username
        reverberation = request.data.get("reverberation", 0)
        rating_scale = request.data.get("rating_scale", "")
        uid = request.data.get("uid", "")
        aac_key_name = request.data.get("aac_key_name", "")
        mp4_key_name = request.data.get("mp4_key_name", "")
        part_jpg_key_name = "part-img.jpg"
        music_id = request.data.get('music_id', "")
        participant_id = request.data.get("participant_id", 0)
        part_to = request.data.get('part_to', "")  # 将要唱的part部分
        is_enable = request.data.get('is_enable', 1)
        invite = request.data.get('invite', invite_li)
        title = request.data.get('title', "")
        ts = request.data.get('ts', 0)
        trim_in = request.data.get("trim", 50)
        bmp_ts = request.data.get("bmp_ts", 8)
        trim = trim_in + 50
        old_part = request.data.get("part_id", 0)
        default_jpg_key = 'default.jpg'

        music = MusicProfiel.objects.get(id=music_id)
        if music:
            pass
        else:
            return json_resp(code=423, msg='not this music')
        banzou_key_name = music.bucket_accompany_key
        segments_key_name = music.segments_key_name
        if participant_id == 0:
            participant_part_one_mp4 = ""
            one_gif_key = default_jpg_key
            one_jpg_key = default_jpg_key

        else:
            part_music = PartSongMusic.objects.get(id=participant_id)
            participant_part_one_mp4 = part_music.one_bucket_key
            one_gif_key = part_music.one_gif_key
            one_jpg_key = part_music.one_jpg_key
            if one_gif_key:
                pass
            else:
                one_gif_key = default_jpg_key
            if one_jpg_key:
                pass
            else:
                one_jpg_key = default_jpg_key
        data = {"uid": uid, "aac_key_name": aac_key_name, "mp4_key_name": mp4_key_name, "user_id": user_id,
                "username": username,
                "invite": invite, "title": title, "banzou_key_name": banzou_key_name,
                "participant_part_one_mp4": participant_part_one_mp4,
                "part_jpg_key_name": part_jpg_key_name,
                "part_to": part_to, "is_enable": is_enable, "music_id": music_id, "participant_id": participant_id,
                "ts": ts, "trim": trim, "bmp_ts": bmp_ts, "segments_key_name": segments_key_name,
                "one_gif_key": one_gif_key, "one_jpg_key": one_jpg_key, "reverberation": reverberation}

        try:
            post_data = PostData.objects.get(uid=uid)
            if post_data.is_ok:
                pass
            else:
                post_data_id = post_data.id
                data['post_data_id'] = post_data_id

                # up_data = {"aac_file": aac_key_name, "mp4_file": mp4_key_name}

                up_to_aws.delay(data)
                # if up_toasw == 200:
                #     pass
                # else:
                #     return json_resp(code=400, msg='error upaws')
                # con_linux(data)
        except:

            post_data = PostData.objects.create(uid=uid, user_id=user_id, username=username, title=title,
                                                music_id=music_id,
                                                participant_id=participant_id, part_to=part_to, is_enable=is_enable,
                                                ts=ts,
                                                trim=trim, bmp_ts=bmp_ts, reverberation_type=reverberation,
                                                invite=invite, aac_key_name=aac_key_name, mp4_key_name=mp4_key_name,
                                                banzou_key_name=banzou_key_name, old_part=old_part,
                                                participant_part_one_mp4=participant_part_one_mp4,
                                                part_jpg_key_name=part_jpg_key_name)
            post_data_id = post_data.id
            data['post_data_id'] = post_data_id
            # con_linux(data)
            up_to_aws.delay(data)
        return json_resp(data="", code=200, msg="wite for result")


class sing_callback(APIView):
    """
        OK
        2018/2/28
        视频合成完成之后回调数据
        """
    permission_classes = (AllowAny,)

    def post(self, request):

        get_data = request.data

        json_data = json.loads(get_data)

        up_aac_bucket_name = "duetin-android-upaac"  # 上传音频
        up_mp4_bucket_name = "duetin-android-upmp4"  # 上传视频
        cuted_bucket_name = "duetin-cuted"  # 视频加处理好干声
        duetin_part_one_bucket = 'duetin-part-one'  # 合成后视频加伴奏加人声未拼接
        part_bucket_name = "duetin-part"  # 合成后视频bucket
        all_bucket_name = 'duetin-chorus'
        hc_aac_bucket_name = 'duetin-hc-voice'
        up_mp4_key_name = json_data["mp4_key_name"]  # 上传的MP4key
        up_aac_key_name = json_data["aac_key_name"]  # 上传的AACkey

        if json_data.has_key("all_compose_mp4"):
            all_music_video_name = json_data["all_compose_mp4"]
            all_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-chorus/compose_vedio/" + \
                            all_music_video_name
            out_all_jpg_name = json_data["all_compose_jpg"]
            all_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-chorus/out_jpg/" + out_all_jpg_name
            out_all_gif_name = json_data['all_compose_gif']
            all_gif_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-all-gif/" + out_all_gif_name
            share_jpg_key = json_data['share_all_jpg']
        else:

            all_music_video_name = json_data["part_compose_mp4"]
            all_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/compose_vedio/" + all_music_video_name
            out_all_jpg_name = json_data["part_one_jpg"]
            all_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/out_jpg/" + out_all_jpg_name
            out_all_gif_name = json_data['part_compose_gif']
            all_gif_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-all-gif/" + out_all_gif_name
            share_jpg_key = json_data['share_part_jpg']

        user_id = json_data['user_id']

        hc_aac_key_name = json_data["hc_aac_out"]
        part_one_mp4 = json_data["part_one_mp4"]
        cuted_out_mp4 = json_data["cuted_out_mp4"]

        title = json_data["title"]
        music_id = json_data["music_id"]
        ts = json_data["ts"]
        participant_id = json_data["participant_id"]
        is_enable = json_data["is_enable"]
        part_to = json_data["part_to"]
        invite = json_data["invite"]
        one_gif_key_name = json_data['one_gif']
        one_jpg_key_name = json_data['part_one_jpg']
        post_uid = json_data['uid']
        try:

            music_info = MusicProfiel.objects.get(id=music_id)
            music_auth = User.objects.get(id=user_id)
        except:
            return json_resp(code=423, msg='not this music')

        part_one_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part-one/" + part_one_mp4

        # partmusic添加记录
        Q_data = QueryDict(mutable=True)

        Q_data['title'] = title
        Q_data['music_info'] = music_info.id
        Q_data['music_auth'] = music_auth.id
        Q_data['vedio_bucket_key'] = up_mp4_key_name
        Q_data['aac_bucket_key'] = up_aac_key_name
        Q_data['hc_aac_key_name'] = hc_aac_key_name
        Q_data['cuted_bucket_key'] = cuted_out_mp4
        Q_data['one_bucket_key'] = part_one_mp4
        Q_data['one_gif_key'] = one_gif_key_name
        Q_data['part_gif_url'] = "https://s3-ap-southeast-1.amazonaws.com/duetin-one-gif/" + one_gif_key_name
        Q_data['one_jpg_key'] = one_jpg_key_name
        Q_data['part_vedio_key'] = all_music_video_name
        Q_data['photo'] = "https://s3-ap-southeast-1.amazonaws.com/duetin-one-jpg/" + one_jpg_key_name
        Q_data['vedio'] = all_vedio_url
        Q_data['part_vedio_url'] = part_one_vedio_url
        Q_data['part'] = part_to
        Q_data['is_enable'] = is_enable

        serializer = CreatePartSongSerializer(data=Q_data)
        if serializer.is_valid():
            part_id = serializer.save()
            uid = part_id.id
        else:
            return serializer.errors

        if participant_id == 0:
            Q_data['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
            Q_data['music_participant_part'] = None
            Q_data['all_music_auth'] = music_auth.id
            Q_data['vedio'] = all_vedio_url
            Q_data["bucket_all_vedio_name"] = part_bucket_name
            Q_data['bucket_all_vedio_key'] = all_music_video_name
            Q_data['photo'] = all_jpg_url
            Q_data['all_gif_key'] = out_all_gif_name
            Q_data['all_gif_url'] = all_gif_url
            Q_data['photo_key_name'] = out_all_jpg_name
            Q_data['share_jpg_key'] = share_jpg_key
            serializer_all = CreateAllSongMusicSerializer(data=Q_data)
            if serializer_all.is_valid():
                all_music = serializer_all.save()

                data = {"id": all_music.id, "type": 2, "feedType": "uploadComplete", "noticeMsgType": 0,
                        "from_user_name": music_auth.username,
                        "musicName": music_info.music_name, "ts": ts}

                mypost = PostData.objects.filter(uid=post_uid).first()
                if mypost:
                    mypost.is_ok = True
                    mypost.all_music_id = all_music.id
                    mypost.all_music_image = out_all_gif_name
                    mypost.save()

                device = FCMDevice.objects.filter(user=music_auth).first()
                device.send_message(data=data)

            else:
                return serializer.errors

            if invite:
                for i in invite:
                    to_user_id = int(i)
                    from_user = music_auth
                    try:
                        to_user = User.objects.get(pk=to_user_id)
                    except:
                        json_resp(code=409, msg="invite error user")

                    title = 'new invite'
                    text = 'invite your join'
                    type = 1
                    post_id = all_music.id
                    link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(post_id)
                    Notification.objects.create(title=title, text=text, from_user=from_user,
                                                to_user=to_user, type=type,
                                                link=link)
                    up_notifactions_count(to_user_id)

                    data = {"id": music_auth.id, "type": 1, "feedType": "", "noticeMsgType": 1,
                            "from_user_name": from_user.username,
                            "musicName": music_info.music_name}

                    device = FCMDevice.objects.filter(user=to_user).first()
                    if device:
                        device.send_message(data=data)
                    else:
                        json_resp(code=424, msg="error push id,can't push Notification")

            return json_resp(data="", code=200, msg="create part ok")
        else:
            try:
                participant_music = PartSongMusic.objects.get(id=participant_id)
            except:
                return json_resp(code=400, msg='no partication music')
            Q_data_all = QueryDict(mutable=True)
            Q_data_all['title'] = title
            Q_data_all['music_info'] = music_info.id
            Q_data_all['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
            Q_data_all['music_participant_part'] = participant_music.id
            Q_data_all['all_music_auth'] = music_auth.id
            Q_data_all['photo_key_name'] = out_all_jpg_name

            Q_data_all['all_gif_key'] = out_all_gif_name
            Q_data_all['all_gif_url'] = all_gif_url

            Q_data_all['photo'] = all_jpg_url
            Q_data_all['vedio'] = all_vedio_url
            Q_data_all["bucket_all_vedio_name"] = all_bucket_name

            Q_data_all['bucket_all_vedio_key'] = all_music_video_name

            Q_data_all['is_enable'] = is_enable
            Q_data_all['share_jpg_key'] = share_jpg_key
            serializer_all = CreateAllSongMusicSerializer(data=Q_data_all)
            if serializer_all.is_valid():
                all_music = serializer_all.save()

                data = {"id": all_music.id, "type": 2, "feedType": "uploadComplete", "noticeMsgType": 0,
                        "from_user_name": music_auth.username,
                        "musicName": music_info.music_name, "ts": ts}

                mypost = PostData.objects.filter(uid=post_uid).first()
                if mypost:
                    mypost.is_ok = True
                    mypost.all_music_id = all_music.id
                    mypost.all_music_image = out_all_gif_name
                    mypost.save()

                device = FCMDevice.objects.filter(user=music_auth).first()
                if device:
                    device.send_message(data=data)
                else:
                    json_resp(code=424, msg="error push id,can't push Notification")

                # 加入视频
                join_title = "new join"
                join_text = "join your post"
                join_type = 1
                join_id = all_music.id
                join_to_user = participant_music.music_auth
                join_link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(join_id)

                Notification.objects.create(title=join_title, text=join_text, from_user=music_auth,
                                            to_user=join_to_user, type=join_type, all_post=all_music,
                                            link=join_link)

                data = {"id": all_music.id, "type": 1, "feedType": "", "noticeMsgType": 2,
                        "from_user_name": music_auth.username,
                        "musicName": music_info.music_name}

                device1 = FCMDevice.objects.filter(user=join_to_user).first()
                if device1:
                    device1.send_message(data=data)
                else:
                    json_resp(code=424, msg="error push id,can't push Notification")
                device1.send_message(data=data)

            else:
                return serializer.errors
            if invite:
                for i in invite:
                    to_user_id = int(i)
                    from_user = music_auth
                    try:

                        to_user = User.objects.get(pk=to_user_id)
                    except:
                        return json_resp(code=409, msg="invite error user")

                    title = 'new invite'
                    text = 'invite your join'
                    type = 2
                    post_id = all_music.id
                    link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(post_id)
                    Notification.objects.create(title=title, text=text, from_user=from_user,
                                                to_user=to_user, type=type, all_post=all_music,
                                                link=link)
                    up_notifactions_count(to_user_id)
                    data = {"id": music_auth.id, "type": 1, "feedType": "", "noticeMsgType": 1,
                            "from_user_name": from_user.username,
                            "musicName": music_info.music_name}

                    device2 = FCMDevice.objects.filter(user=to_user).first()
                    if device2:
                        device2.send_message(data=data)
                    else:
                        json_resp(code=424, msg="invite error push id,can't push Notification")
                    device2.send_message(data=data)

            return json_resp(code=200, msg="create all ok")


class Handle_Callback(APIView):
    """
    OK
    2018/2/28
    视频是否处理完毕
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code_lag = check_lan(request)
        user = request.user
        username = user.username

        logger_in.error("----------------------------------->")
        logger_in.error("username:" + username)

        uid_list = request.data.get('uid', "")

        logger_in.error(type(uid_list))
        logger_in.error(uid_list)

        data = []
        if uid_list:
            for uid in uid_list:

                logger_in.error("start_uid:" + uid)

                data_di = {}
                my_post = PostData.objects.filter(uid=uid).first()
                if my_post:
                    logger_in.error('uid:' + uid + " ok")
                    is_ok = my_post.is_ok
                    logger_in.error(is_ok)

                    if is_ok:
                        if my_post.all_music_image:
                            photo = allgif_url + my_post.all_music_image
                            id = my_post.all_music_id
                            post_uid = my_post.uid
                        else:
                            photo = ""
                            id = my_post.all_music_id
                            post_uid = my_post.uid
                        data_di["uid"] = post_uid
                        data_di['id'] = id
                        data_di['photo'] = photo
                        data.append(data_di)

                        logger_in.error("photo:" + photo)
                    else:
                        logger_in.error("uid:" + uid + " is not ok")
                else:
                    logger_in.error("uid:" + uid + " not found")

            return json_resp(code=200, msg='ok', data=data)
        else:
            return json_resp(code=499, msg=code_lag['499'])


class Search_Index_View(APIView):
    """新版搜索页面，推荐的歌曲列表"""
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return MusicProfiel.objects.filter(is_delete=False, is_online=True)

    def get(self, request):
        music_pro = self.get_object().order_by('-sort', '-rank', '-view_count')

        return js_resp_paging(music_pro, request, MusicProfileSingerSerializer, pages=20)


class Search_User_View(APIView):
    """
    新版本搜索页面，选择男女，性别搜索匹配
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        part_music = PartSongMusic.objects.select_related().filter(is_enable=1, is_delete=0)
        return part_music

    def post(self, request):
        code_lag = check_lan(request)

        try:
            now_year = datetime.datetime.now().strftime("%Y")
            sex = int(request.data.get("sex"))
            birth_mix = request.data.get('birth_mix')
            birth_max = request.data.get('birth_max')

            max_year = int(now_year) - int(birth_mix)+1
            max_timeArray = time.strptime(str(max_year), "%Y")
            max_timeStamp = int(time.mktime(max_timeArray))*1000

            mix_year = int(now_year) - int(birth_max)
            mix_timeArray = time.strptime(str(mix_year), "%Y")
            mix_timeStamp = int(time.mktime(mix_timeArray))*1000

            list_part = []
            music_info = MusicProfiel.objects.select_related().filter(
                Q(is_online=1) | Q(view_count__gt=0)).order_by(
                '-view_count')[:100]
            music_t10 = list(music_info[:10])
            random.shuffle(music_t10)
            music_t50 = list(music_info[10:50])
            random.shuffle(music_t50)
            music_t100 = list(music_info[50:100])
            random.shuffle(music_t100)
            # music_t200=list(music_info[100:200])
            music_list = music_t10 + music_t50 + music_t100

            for music in music_list:

                # part_music = PartSongMusic.objects.select_related().filter(is_enable=1, is_delete=0,
                # music_info=music)
                # if part_music:
                #     cho_part = random.choice(part_music)
                #     list_part.append(cho_part)
                # else:
                #     pass


                if sex == 9:

                    part_music = PartSongMusic.objects.select_related().filter(
                        Q(music_auth__new_birth__range=(mix_timeStamp, max_timeStamp)), is_enable=1,
                        music_info=music,
                        is_delete=0)
                    # if part_music:
                    #     cho_part = random.choice(part_music)
                    #     list_part.append(cho_part)
                    # else:
                    #     pass
                else:
                    part_music = PartSongMusic.objects.select_related().filter(
                        Q(music_auth__new_birth__range=(mix_timeStamp, max_timeStamp)), is_enable=1, is_delete=0,
                        music_auth__sex=sex, music_info=music)

                if part_music:
                    cho_part = random.choice(part_music)
                    list_part.append(cho_part)
                else:
                    pass
            if sex==9:
                red_part_music = PartSongMusic.objects.select_related().filter(
                    Q(music_auth__new_birth__range=(mix_timeStamp, max_timeStamp)), is_enable=1, is_delete=0).order_by("?")[:200]

            else:
                red_part_music = PartSongMusic.objects.select_related().filter(
                    Q(music_auth__new_birth__range=(mix_timeStamp, max_timeStamp)), is_enable=1, is_delete=0,
                    music_auth__sex=sex).order_by("?")[:200]

            for obj_r in red_part_music:
                list_part.append(obj_r)

            func = lambda x, y: x if y in x else x + [y]

            list_objs = reduce(func, [[], ] + list_part)

            return js_resp_paging(objs=list_objs, request=request, serializer_obj=PartRandomSerializer, pages=20)
        except:
            return json_resp(code=499, msg=code_lag['499'])


            # def post(self, request):
            #     code_lag = check_lan(request)
            #
            #     try:
            #         now_year = datetime.datetime.now().strftime("%Y")
            #         sex = int(request.data.get("sex"))
            #         birth_mix = request.data.get('birth_mix')
            #         birth_max = request.data.get('birth_max')
            #
            #         max_year = int(now_year) - int(birth_mix)
            #         max_timeArray = time.strptime(str(max_year), "%Y")
            #         max_timeStamp = int(time.mktime(max_timeArray))
            #
            #         mix_year = int(now_year) - int(birth_max)
            #         mix_timeArray = time.strptime(str(mix_year), "%Y")
            #         mix_timeStamp = int(time.mktime(mix_timeArray))
            #
            #         if sex == 9:
            #             part_music = PartSongMusic.objects.select_related().filter(
            #                 Q(music_auth__new_birth__range=(mix_timeStamp, max_timeStamp)), is_enable=1, is_delete=0)
            #         else:
            #
            #             part_music = PartSongMusic.objects.select_related().filter(
            #                 Q(music_auth__new_birth__range=(mix_timeStamp, max_timeStamp)), is_enable=1, is_delete=0,
            #                 music_auth__sex=sex)
            #         return js_resp_paging(objs=part_music, request=request, serializer_obj=PartRandomSerializer,
            # pages=20)
            #     except:
            #         return json_resp(code=499, msg=code_lag['499'])


class Sing_Random_View(APIView):
    """
    歌曲随机匹配
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        list_part = []
        music_info = MusicProfiel.objects.select_related().filter(Q(is_online=1) | Q(view_count__gt=0)).order_by(
            '-view_count')[:100]
        music_t10 = list(music_info[:10])
        random.shuffle(music_t10)
        music_t50 = list(music_info[10:50])
        random.shuffle(music_t50)
        music_t100 = list(music_info[50:100])
        random.shuffle(music_t100)
        # music_t200=list(music_info[100:200])
        music_list = music_t10 + music_t50 + music_t100

        for music in music_list:

            part_music = PartSongMusic.objects.select_related().filter(is_enable=1, is_delete=0, music_info=music)
            if part_music:
                cho_part = random.choice(part_music)
                list_part.append(cho_part)
            else:
                pass

        red_part_music = PartSongMusic.objects.select_related().filter(is_enable=1, is_delete=0)[:200]
        for obj_r in red_part_music:
            list_part.append(obj_r)

        func = lambda x, y: x if y in x else x + [y]

        list_objs = reduce(func, [[], ] + list_part)
        return js_resp_paging(objs=list_objs, request=request, serializer_obj=PartRandomSerializer, pages=20)

    def post(self, request):
        music_id = request.data.get("music_id")
        try:
            music = MusicProfiel.objects.get(id=music_id)
            part_music = PartSongMusic.objects.select_related().filter(is_enable=1, is_delete=0, music_info=music)
            return js_resp_paging(objs=part_music, request=request, serializer_obj=PartRandomSerializer, pages=20)
        except:
            return json_resp(code=483, msg="error music")


class Up_Trim_View(APIView):
    """
    2018/3/27
    更新手机延迟
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code_lag = check_lan(request)
        try:
            data = request.data
            devicename = data.get('devicename')
            model = data.get('model')
            manufacturer = data.get('manufacturer')
            os = data.get('os')
            trim = data.get('trim')
            error_count = data.get('error_count')

            mobile_l = MobileVersion.objects.filter(mobile_yj_name=devicename, mobile_version=model,
                                                    mobile_brand=manufacturer,
                                                    mobile_edition=os).first()

            if mobile_l:
                mobile_l.delay_time = trim
                error_count_ser = mobile_l.error_count
                mobile_l.error_count = int(error_count) + error_count_ser
                mobile_l.save()
            else:
                mobile_id = MobileVersion.objects.create(mobile_yj_name=devicename, mobile_version=model,
                                                         mobile_brand=manufacturer,
                                                         mobile_edition=os, delay_time=trim, error_count=error_count)

            return json_resp(code=200, msg='ok')
        except:
            return json_resp(code=499, msg=code_lag['499'])
