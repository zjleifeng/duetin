#!/usr/bin/env python
# encoding: utf-8
import os
import logging
import time
import random
import oss2
import urllib
import json

import datetime


def dispose_all_ffmpeg(event, context):
    """
    处理allmusic部分合成视频左右拼接合成，截取图片
    :param request: 
    :param auth_vedio: auth部分的MP4（伴奏+干声+视频）
    :param participant_video: 参与者(我)部分MP4（干声+视频）
    :param lyc_time: 取图时间点
    :return: 
    """
    json_string = json.dumps(event)
    evt = json.loads(json_string)

    fn = time.strftime('%Y%m%d%H%M%S')
    user_name = evt['username']
    my_post_url = evt['my_mp4_url']
    part_music_url = evt['part_music_url']
    # banzou_url = evt['banzou']

    # 下载我的歌曲MP4
    filedir = '/tmp/'
    my_post_url_list = my_post_url.split('/')
    my_file_path = filedir + my_post_url_list[-1]

    urllib.urlretrieve(my_post_url, my_file_path)

    # 下载伴奏
    # banzouurl_list = banzou_url.split('/')
    # banzoufile_path = '/tmp/' + banzouurl_list[-1]
    # urllib.urlretrieve(banzou_url, banzoufile_path)

    # 下载对方歌曲MP4
    part_music_list = part_music_url.split('/')
    part_file_path = filedir + part_music_list[-1]

    urllib.urlretrieve(part_music_url, part_file_path)

    out_vedio_name = 'mp4_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    # out_aac_name = 'aac_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    # out_voice_name = 'voice_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    # out_media_name = 'media_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    # part_music_vedio_name = 'part_music_mp4' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000,
    #                                                                                                99999) + '.mp4'
    # out_part_jpg_name = 'jpg_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.jpg'

    all_music_video_name = 'allmusic_mp4_' + user_name + '_' + fn + '_%d' % random.randint(10000,
                                                                                           99999) + '.mp4'
    out_all_jpg_name = 'allmusic_jpg_' + user_name + '_' + fn + '_%d' % random.randint(10000,
                                                                                       99999) + '.jpg'

    out_vedio_path = filedir + out_vedio_name  # 裁剪后视频
    # out_aac_path = filedir + out_aac_name  # 视频取出的音频
    # out_voice_path = filedir + out_voice_name  # 音频和伴奏的合成
    # out_media_path = filedir + out_media_name  # 视频取出的视频无声音
    # part_music_vedio_path = filedir + part_music_vedio_name  # 合成后的视频
    # out_part_jpg = filedir + out_part_jpg_name  # 截图

    all_music_video_path = filedir + all_music_video_name  # 合唱合成视频
    out_all_jpg_path = filedir + out_all_jpg_name  # 合唱合成图片

    try:
        # part部分合成好的视屏+刚刚拍摄剪切的视频合成新的视频


        # 裁剪视频得到裁剪的视频加干声MP4

        os.system(
            "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -strict -2 -vf scale=320:360,crop=320:360:20:4 -ac 2 %s" % (
                my_file_path, out_vedio_path))
        # print "out_vedio_path:%s" % out_vedio_path
        # # 取音频
        # os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -vn -ac 2 %s" % (
        #     out_vedio_path, out_aac_path))
        # print "out_aac_path:%s" % out_aac_path
        # # 取视频
        # os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -an %s" % (
        #     out_vedio_path, out_media_path))
        # print "out_media_path:%s" % out_media_path
        #
        # # 音频伴奏合成
        # os.system(
        #     "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -filter_complex amix=inputs=2:duration=longest:dropout_transition=2 -ac 2 %s" % (
        #         out_aac_path, banzoufile_path, out_voice_path))
        # print "out_voice_path:%s" % out_voice_path
        #
        # # 音频视频合成
        # os.system(
        #     "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -ac 2 %s" % (
        #         out_media_path, out_voice_path, part_music_vedio_path))
        # print "part_music_vedio_path:%s" % part_music_vedio_path
        #
        # # 截图
        # os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -y -f image2 -ss 8 -t 0.001 -s 320x360 %s" % (
        #     part_music_vedio_path, out_part_jpg))
        # print "out_part_jpg:%s" % out_part_jpg

        # 合成视频左边永远是发布者


        os.system(
            "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -filter_complex \"[0:v]pad=w=iw*2:h=ih[b];[b][1:v]overlay=x=W/2\" -filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -ac 2 %s" % (
                out_vedio_path, part_file_path, all_music_video_path))
        # print "start all"
        # print "all_music_video_path:%s" % all_music_video_path

        # 对新合成视频截图
        os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -y -f image2 -ss 8 -t 0.001 -s 640x360 %s" % (
            all_music_video_path, out_all_jpg_path))
        # print "out_all_jpg_path:%s" % out_all_jpg_path

        try:
            auth = oss2.Auth('LTAIXeFWeGVCQS3r', 'NNgpxxKyIfAr4J9RJ4N4AHlYvX7a9e')
            # print "shangchuan part"
            # bucket_part = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'duetin-part')
            # with open(part_music_vedio_path, 'rb') as filepart_v:
            #     bucket_part.put_object('compose_vedio/' + part_music_vedio_name, filepart_v)

            # with open(out_part_jpg, 'rb') as filepart_j:
            #     bucket_part.put_object('out_jpg/' + out_part_jpg_name, filepart_j)
            #
            # part_music_mp4_path = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/compose_vedio/' + part_music_vedio_name
            # part_music_jpg_path = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/out_jpg/' + out_part_jpg_name

            # print "shangchuan all"

            bucket_all = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'duetin-all')
            with open(all_music_video_path, 'rb') as file_all_v:
                bucket_all.put_object('compose_vedio/' + all_music_video_name, file_all_v)

            with open(out_all_jpg_path, 'rb') as fileobj:
                bucket_all.put_object('out_jpg/' + out_all_jpg_name, fileobj)

            all_music_mp4_path = 'http://duetin-all.oss-cn-shanghai.aliyuncs.com/compose_vedio/compose_vedio/' + all_music_video_name
            all_music_jpg_path = 'http://duetin-all.oss-cn-shanghai.aliyuncs.com/compose_vedio/out_jpg/' + out_all_jpg_name

            l = {
                "all_music_mp4_path": all_music_mp4_path,
                "all_music_jpg_path": all_music_jpg_path
            }

            os.system('rm  -rf /tmp/*')
            return json.dumps(l)
        except oss2.exceptions.code as e:
            os.system('rm  -rf /tmp/*')
            data = {"code": 400, "msg": e, "data": ""}

            return json.dumps(data)
    except:
        os.system('rm  -rf /tmp/*')

        data = {"code": 400, "msg": "ffmpeg error", "data": ""}

        return json.dumps(data)









    # json_string = json.dumps(event)
    # evt = json.loads(json_string)
    #
    # fn = time.strftime('%Y%m%d%H%M%S')
    # user_name = evt['username']
    # my_post_url = evt['my_mp4_url']
    # part_music_url = evt['part_music_url']
    # banzou_url = evt['banzou']
    # # participant_post_url=evt["participant_vedio"]
    # # part_to=evt["patr_to"]
    # # 下载我的歌曲MP4
    # filedir = '/tmp/'
    # my_post_url_list = my_post_url.split('/')
    # my_file_path = filedir + my_post_url_list[-1]
    #
    # urllib.urlretrieve(my_post_url, my_file_path)
    #
    # #下载伴奏
    # banzouurl_list = banzou_url.split('/')
    # banzoufile_path = '/tmp/' + banzouurl_list[-1]
    # urllib.urlretrieve(banzou_url, banzoufile_path)
    #
    # # 下载对方歌曲MP4
    # part_music_list = part_music_url.split('/')
    # part_file_path = filedir + part_music_list[-1]
    #
    # urllib.urlretrieve(part_music_url, part_file_path)
    #
    # out_vedio_name = 'mp4_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    # out_aac_name = 'aac_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    # out_voice_name = 'voice_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    # out_media_name = 'media_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    # part_music_vedio_name = 'part_music_mp4' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000,
    #                                                                                                99999) + '.mp4'
    # out_part_jpg_name = 'jpg_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.jpg'
    #
    # all_music_video_name = 'allmusic_mp4_' + user_name + '_' + fn + '_%d' % random.randint(10000,
    #                                                                                        99999) + '.mp4'
    # out_all_jpg_name = 'allmusic_jpg_' + user_name + '_' + fn + '_%d' % random.randint(10000,
    #                                                                                    99999) + '.jpg'
    #
    # out_vedio_path = filedir + out_vedio_name  # 裁剪后视频
    # out_aac_path = filedir + out_aac_name  # 视频取出的音频
    # out_voice_path = filedir + out_voice_name  # 音频和伴奏的合成
    # out_media_path = filedir + out_media_name  # 视频取出的视频无声音
    # part_music_vedio_path = filedir + part_music_vedio_name  # 合成后的视频
    # out_part_jpg = filedir + out_part_jpg_name  # 截图
    #
    # all_music_video_path = filedir + all_music_video_name#合唱合成视频
    # out_all_jpg_path = filedir + out_all_jpg_name#合唱合成图片
    #
    # try:
    #     # part部分合成好的视屏+刚刚拍摄剪切的视频合成新的视频
    #     part = int(part_to)
    #
    #     # 裁剪视频得到裁剪的视频加干声MP4
    #
    #     os.system(
    #         "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -strict -2 -vf scale=320:360,crop=320:360:20:4 -ac 2 %s" % (
    #             my_file_path, out_vedio_path))
    #     print "out_vedio_path:%s"%out_vedio_path
    #     # 取音频
    #     os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -vn -ac 2 %s" % (
    #         out_vedio_path, out_aac_path))
    #     print "out_aac_path:%s"%out_aac_path
    #     # 取视频
    #     os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -an %s" % (
    #         out_vedio_path, out_media_path))
    #     print "out_media_path:%s"%out_media_path
    #
    #     # 音频伴奏合成
    #     os.system(
    #         "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -filter_complex amix=inputs=2:duration=longest:dropout_transition=2 -ac 2 %s" % (
    #             out_aac_path, banzoufile_path, out_voice_path))
    #     print "out_voice_path:%s"%out_voice_path
    #
    #     # 音频视频合成
    #     os.system(
    #         "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -ac 2 %s" % (
    #             out_media_path, out_voice_path, part_music_vedio_path))
    #     print "part_music_vedio_path:%s"%part_music_vedio_path
    #
    #     # 截图
    #     os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -y -f image2 -ss 8 -t 0.001 -s 320x360 %s" % (
    #         part_music_vedio_path, out_part_jpg))
    #     print "out_part_jpg:%s"%out_part_jpg
    #
    #     # 合成视频左边永远是发布者
    #
    #
    #     # os.system(
    #     #     "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -filter_complex \"[0:v]pad=w=iw*2:h=ih[b];[b][1:v]overlay=x=W/2\" -filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -ac 2 %s" % (
    #     #         part_music_vedio_path, part_file_path, all_music_video_path))
    #     # print "start all"
    #     # print "all_music_video_path:%s"%all_music_video_path
    #     #
    #     # # elif part == 0:
    #     # #     os.system(
    #     # #         "/ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -filter_complex \"[0:v]pad=w=iw*2:h=ih[b];[b][1:v]overlay=x=W/2\" -filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -ab 128k -ar 44100 -ac 1 -r 15 -b 150k %s" % (
    #     # #             music_participant_part_vedio_path, music_auth_part_vedio_path, compose_video_path))
    #     # # 对新合成视频截图
    #     # os.system("/usr/local/bin/ffmpeg -i %s -y -f image2 -ss 8 -t 0.001 -s 640x360 %s" % (
    #     #     all_music_video_path, out_all_jpg_path))
    #     # print "out_all_jpg_path:%s"%out_all_jpg_path
    #
    #
    #     try:
    #         auth = oss2.Auth('LTAIXeFWeGVCQS3r', 'NNgpxxKyIfAr4J9RJ4N4AHlYvX7a9e')
    #         print "shangchuan part"
    #         bucket_part = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'duetin-part')
    #         with open(part_music_vedio_path, 'rb') as filepart_v:
    #             bucket_part.put_object('compose_vedio/' + part_music_vedio_name, filepart_v)
    #
    #         with open(out_part_jpg, 'rb') as filepart_j:
    #             bucket_part.put_object('out_jpg/' + out_part_jpg_name, filepart_j)
    #
    #         part_music_mp4_path = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/compose_vedio/' + part_music_vedio_name
    #         part_music_jpg_path = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/out_jpg/' + out_part_jpg_name
    #
    #         print "shangchuan all"
    #         #
    #         # bucket_all = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'duetin-all')
    #         # with open(all_music_video_path, 'rb') as file_all_v:
    #         #     bucket_all.put_object('compose_vedio/' + all_music_video_name, file_all_v)
    #         #
    #         # with open(out_all_jpg_path, 'rb') as fileobj:
    #         #     bucket_all.put_object('out_jpg/' + out_all_jpg_name, fileobj)
    #         #
    #         # all_music_mp4_path = 'http://duetin-all.oss-cn-shanghai.aliyuncs.com/compose_vedio/compose_vedio/' + all_music_video_name
    #         # all_music_jpg_path = 'http://duetin-all.oss-cn-shanghai.aliyuncs.com/compose_vedio/out_jpg/' + out_all_jpg_name
    #
    #         l = {
    #             "part_music_mp4_path": part_music_mp4_path,
    #             "part_music_jpg_path": part_music_jpg_path
    #             # "all_music_mp4_path":all_music_mp4_path,
    #             # "all_music_jpg_path":all_music_jpg_path
    #         }
    #
    #         os.system('rm  -rf /tmp/*')
    #         return json.dumps(l)
    #     except oss2.exceptions.code as e:
    #         os.system('rm  -rf /tmp/*')
    #         data = {"code": 400, "msg": e, "data": ""}
    #
    #         return json.dumps(data)
    # except:
    #     os.system('rm  -rf /tmp/*')
    #
    #     data = {"code": 400, "msg": "ffmpeg error", "data": ""}
    #
    #     return json.dumps(data)
    #     # if os.path.exists(compose_video_path) and os.path.exists(out_jpg_path):
    #     #
    #     #     path_data = {'out_vedio_name': 'media/music/' + compose_video_name,
    #     #                  'out_jpg_name': 'media/music/' + out_jpg_name}
    #     #     ret['data'] = path_data
    #     #     return ret
    #     # else:
    #     #     return json_resp(code=400, msg="error")
