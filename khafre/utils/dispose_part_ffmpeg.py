#!/usr/bin/env python
# encoding: utf-8
import os
import logging
import time
import random
import oss2
import urllib
import json
import boto3
import botocore
import datetime


def dispose_part_ffmpeg(event, context):
    """
    处理part部分上传后的MP4进行裁剪,音频视频分离，合成，取图
    """

    json_string = json.dumps(event)
    evt = json.loads(json_string)
    # file_path = '/tmp/'
    filedir = '/tmp/'
    fn = time.strftime('%Y%m%d%H%M%S')
    user_name = evt['username']

    bucket_name = evt['bucket_name']
    down_key = evt['down_key']
    my_file_path = filedir + "luzhi.mp4"

    banzou_bucket_name = evt['banzou_bucket_name']
    banzou_bucket_key = evt['banzou_bucket_key']
    banzoufile_path = filedir + "banzou.mp4"

    s3 = boto3.client('s3', region_name="ap-southeast-1",
                      aws_access_key_id="AKIAIE665KY6G6OJARGA",
                      aws_secret_access_key="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")

    try:
        s3.download_file(bucket_name, down_key, filedir + "luzhi.mp4")
        s3.download_file(banzou_bucket_name, banzou_bucket_key, filedir + "banzou.mp4")

    except:
        return None

    if not os.path.exists(my_file_path) and os.path.exists(banzoufile_path):
        return None
    # url = evt['url']
    # url_list = url.split('/')
    # file_path = '/tmp/' + url_list[-1]

    # 从S3下载
    # BUCKET_NAME = 'duetin-part'  # replace with your bucket name
    # KEY = url_list[-1]  # replace with your object key

    # try:
    #     s3.Bucket(BUCKET_NAME).download_file(KEY,'/tmp/'+KEY)
    # except botocore.exceptions.ClientError as e:
    #     if e.response['Error']['Code'] == "404":
    #         print("The object does not exist.")
    #     else:
    #         raise

    # urllib.urlretrieve(url, file_path)
    #
    # banzou_url = evt['banzou']
    # banzouurl_list = banzou_url.split('/')
    # banzoufile_path = '/tmp/' + banzouurl_list[-1]
    # urllib.urlretrieve(banzou_url, banzoufile_path)

    out_vedio_name = 'mp4_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    out_aac_name = 'aac_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    out_voice_name = 'voice_out' + '_' + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.aac'
    out_media_name = 'media_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    compose_vedio_name = 'mp4_compose' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.mp4'
    out_jpg_name = 'jpg_out' + "_" + user_name + '_' + fn + '_%d' % random.randint(10000, 99999) + '.jpg'

    out_vedio_path = filedir + out_vedio_name  # 裁剪后视频
    out_aac_path = filedir + out_aac_name  # 视频取出的音频
    out_voice_path = filedir + out_voice_name  # 音频和伴奏的合成
    out_media_path = filedir + out_media_name  # 视频取出的视频无声音
    compose_vedio_path = filedir + compose_vedio_name  # 合成后的视频
    out_jpg_path = filedir + out_jpg_name  # 截图

    UP_BUCKET_PART_NAME = "duetin-part"
    UP_VEDIO_PART_KEY = "compose_vedio/" + compose_vedio_name
    UP_JPG_PART_KEY = "out_jpg/" + out_jpg_name
    try:

        # 裁剪视频得到裁剪的视频加干声MP4

        os.system(
            "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -strict -2 -vf scale=320:360,crop=320:360:20:4 -r 15 -b 150k -ab 128k -ar 44100 -ac 2 %s" % (
                my_file_path, out_vedio_path))
        # 取音频
        os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -vn -y -acodec aac -ab 128k -ar 44100 -ac 2 %s" % (
            out_vedio_path, out_aac_path))

        # 取视频
        os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -an -y -vcodec copy -r 15 -b 150k %s" % (
            out_vedio_path, out_media_path))

        # 音频伴奏合成
        os.system(
            "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -filter_complex amix=inputs=2:duration=longest:dropout_transition=2  -ab 128k -ar 44100 -ac 2 %s" % (
                out_aac_path, banzoufile_path, out_voice_path))

        # 音频视频合成
        os.system(
            "ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -i %s -vcodec copy -acodec copy -r 15 -b 150k -ab 128k -ar 44100 -ac 2 %s" % (
                out_media_path, out_voice_path, compose_vedio_path))
        # 截图
        os.system("ffmpeg-3.3.2-64bit-static/ffmpeg -i %s -y -f image2 -ss %d -t 0.001 -s 320x360 %s" % (
            compose_vedio_path, 8, out_jpg_path))

        # 上传到S3

        # 上传原始裁剪视频
        s3.upload_file(out_vedio_path , "duetin-cuted", out_vedio_name)
        # 上传合成视频
        s3.upload_file(compose_vedio_path , UP_BUCKET_PART_NAME, UP_VEDIO_PART_KEY)
        # 上传视频截图
        s3.upload_file(out_jpg_path , UP_BUCKET_PART_NAME, UP_JPG_PART_KEY)

        caijian_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-cuted/" + out_vedio_name
        part_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/compose_vedio/" + compose_vedio_name
        part_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/out_jpg/" + out_jpg_name

        result={

        }

        res = {
            "caijian_vedio_url": caijian_vedio_url,
            "part_vedio_url": part_vedio_url,
            "part_jpg_url": part_jpg_url
        }

        os.system('rm  -rf /tmp/*')
        return json.dumps(res)
    except oss2.exceptions.code as e:
        os.system('rm  -rf /tmp/*')
        data = {"code": 400, "msg": e, "data": ""}

        return None
        # 上传到阿里OSS
        # try:
        #     auth = oss2.Auth('LTAIXeFWeGVCQS3r', 'NNgpxxKyIfAr4J9RJ4N4AHlYvX7a9e')
        #
        #     bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'duetin-part')
        #     with open(compose_vedio_path, 'rb') as fileobj:
        #         bucket.put_object('compose_vedio/' + compose_vedio_name, fileobj)
        #
        #     with open(out_jpg_path, 'rb') as fileobj:
        #         bucket.put_object('out_jpg/' + out_jpg_name, fileobj)
        #
        #     url_path = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/compose_vedio/' + compose_vedio_name
        #     url_jpg = 'http://duetin-part.oss-cn-shanghai.aliyuncs.com/out_jpg/' + out_jpg_name
        #
        #     l = {
        #         "compose_vedio": url_path,
        #         "out_jpg": url_jpg
        #     }
        #
        #     os.system('rm  -rf /tmp/*')
        #     return json.dumps(l)
        # except oss2.exceptions.code as e:
        #     os.system('rm  -rf /tmp/*')
        #     data = {"code": 400, "msg": e, "data": ""}
        #
        #     return json.dumps(data)

# except:
# os.system('rm  -rf /tmp/*')
#
# data = {"code": 400, "msg": "ffmpeg error", "data": ""}
#
# return json.dumps(data)
