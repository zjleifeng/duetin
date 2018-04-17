#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: tasks.py.py
@time: 2017/6/1 下午1:33
@SOFTWARE:PyCharm
"""

from __future__ import absolute_import
from celery import shared_task, platforms
import os, time, random, re
from khufu import settings
from khafre.utils.json_response import json_resp
import shutil
from app_auth.models import User
from dao.models.music import MusicProfiel, PartSongMusic, AllSongMusic, Notification, AboutyouNotification
from khafre.main.serilizers import AllSongMusicSearchSerializer, \
    CreatePartSongSerializer, CreateAllSongMusicSerializer

from khafre.message.serializers import Create_AboutyouNotificationSer,Create_FollowerNotificationSerializer
from django.utils import timezone
from django.core.mail import send_mail
from khufu.celery import app
from khafre.main.cache_manager import up_notifactions_count
from fcm_django.models import FCMDevice
import requests

# from khafre.utils.signals import create_A_handler,create_N_handler
from django.db.models.signals import post_save

from django.dispatch import receiver

platforms.C_FORCE_ROOT = True
from relationships import Relationship
import json
import boto3
from khufu.settings import redis_ship, client_lambda, client_s3
from django.http.request import QueryDict

r = Relationship(redis_ship)


# @receiver(post_save, sender=AboutyouNotification)
def create_A_handler(sender, instance, created, **kwargs):
    AboutyouNotification.objects.create(title="2wwwe")

    print "send msg start"
    to_user = instance.to_user
    user_id = to_user.id
    device = FCMDevice.objects.filter(id=user_id).first()
    device.send_message(data={"test": "test"})


# @receiver(post_save, sender=Notification)
def create_N_handler(sender, instance, created, **kwargs):
    to_user = instance.to_user
    user_id = to_user.id
    device = FCMDevice.objects.filter(id=user_id).first()
    device.send_message(data={"test": "test"})

@app.task
def send_register_url_email(obj):
    print 'sendemail start'
    if obj:
        url = "http://api.sendcloud.net/apiv2/mail/sendtemplate"
        try:
            user = User.objects.get(id=obj)

            user_email = user.email
            rt = user.registeremailtoken
            expire_local_time = timezone.localtime(rt.expire_time)

            # expire_local_time = datetime.datetime.utcnow().replace(tzinfo=utc)
            register_email_url = "http://duetin.com/api/v1/account/register_email/{0}/{1}/".format(rt.dynamic_url,
                                                                                                   rt.entry_token)

            # email_content = (
            #     """
            #     "Hi, {username}<br>"
            #
            #     "这是来自duetin的注册用户邮箱验证信息，<br>"
            #     "为了您的账户安全，请尽快验证邮箱信息！<br>"
            #     "点击以下链接进入验证或者复制链接到浏览器打开<br>"
            #
            #     "有效期至: {expire_time}。"<br>
            #     "{register_email_url}"<br>
            #
            #     "验证码: {entry_token}"<br>
            #
            #     "感謝謝您的使用!<br>"
            #     "----------------------------------------------<br>"
            #     "duetin"
            #     """
            # ).format(
            #     username=user.username,
            #     expire_time=expire_local_time.strftime("%Y-%m-%d %H:%M"),
            #     register_email_url=register_email_url,
            #     entry_token=rt.entry_token
            # )
            # html = '<html><body><p>{}</p></body></html>'.format(email_content)
            xsmtpapi = {
                'to': [user_email],
                'sub': {
                    '%username%': [user.username],
                    '%reg-url%': [register_email_url],
                }
            }
            params = {
                "apiUser": "superman",  # 使用apiUser和apiKey进行验证
                "apiKey": "1zXr7nLe6LGRl2lZ",
                "templateInvokeName": "duetin_reg",
                "xsmtpapi": json.dumps(xsmtpapi),
                "from": "service@duetin.com",  # 发信人, 用正确邮件地址替代
                "fromName": "duetin team",
                "subject": "Welcome to Duetin!"
            }
            r = requests.post(url, files={}, data=params)
            print r.text
            return True
        except:
            return False


@app.task
def send_reset_password_url_email_to(obj):
    print "send email start"
    url = "http://api.sendcloud.net/apiv2/mail/sendtemplate"

    if obj:
        try:
            user = User.objects.get(id=obj)
            user_email = user.email
            rt = user.resetpasswordtoken
            expire_local_time = timezone.localtime(rt.expire_time)
            username = user.username
            reset_password_url = "http://duetin.com/api/v1/account/reset_password/" + rt.dynamic_url
            expire_time = expire_local_time.strftime("%Y-%m-%d %H:%M")

            entry_token = rt.entry_token
            xsmtpapi = {
                'to': [user_email],
                'sub': {
                    '%username%': [username],
                    '%reset_url%': [reset_password_url],
                    '%expire_time%':[expire_time],
                    '%entry_token%':[entry_token],

                }
            }
            params = {
                "apiUser": "superman",  # 使用apiUser和apiKey进行验证
                "apiKey": "1zXr7nLe6LGRl2lZ",
                "templateInvokeName": "duetin_findpsd",
                "xsmtpapi": json.dumps(xsmtpapi),
                "from": "service@duetin.com",  # 发信人, 用正确邮件地址替代
                "fromName": "duetin team",
                "subject": "reset duetin password!"
            }
            # email_content = (
            #     "Hi, {username}\n\n"
            #
            #     "這是重置密碼的信件，點選下列連結可以進入重置頁面，\n"
            #     "如果您沒有使用忘記密碼的功能，請忽略本信。\n"
            #     "該連結必須輸入驗證碼用以驗證。\n\n"
            #
            #     "下列為密碼重置連結，連結有效時間至: {expire_time}。\n"
            #     "{reset_password_url}\n\n"
            #
            #     "驗證碼: {entry_token}\n\n"
            #
            #     "感謝謝您的使用!\n"
            #     "----------------------------------------------\n"
            #     "Share Class 團隊"
            # ).format(
            #     username=user.username,
            #     expire_time=expire_local_time.strftime("%Y-%m-%d %H:%M"),
            #     reset_password_url="http://duetin.com/api/v1/account/reset_password/" + rt.dynamic_url,
            #     entry_token=rt.entry_token
            # )
            # html = '<html><body><p>{}</p></body></html>'.format(email_content)
            # params = {"apiUser": "superman",
            #           "apiKey": "1zXr7nLe6LGRl2lZ",
            #           "from": "service@duetin.com",
            #           "fromName": "duetin team",
            #           "to": user_email,
            #           "subject": "感谢注册duetin！",
            #           "html": html,
            #           }
            r = requests.post(url, files={}, data=params)

        except:
            return "send reg mail error"

    else:
        return "no user"


# @receiver(post_save, sender=ALLMusicPraise, dispatch_uid='ALLMusicPraise_created_save')
@app.task
def praise_msg(from_user_id, to_user_id, post_id):
    # to_user = instance.music.all_music_auth
    # from_user = instance.owner
    # post_id = instance.music.id

    try:
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)
        post = AllSongMusic.objects.get(id=post_id)
        title = 'new praise'
        text = 'praise your post'
        type = 4
        link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(post.id)

        Q_data = QueryDict(mutable=True)
        Q_data['title'] = title
        Q_data['text'] = text
        Q_data['link'] = link
        Q_data['from_user'] = from_user.id
        Q_data['to_user'] = to_user.id
        Q_data['post'] = post_id
        Q_data['all_post'] = post.id
        Q_data['type'] = type
        serializer = Create_AboutyouNotificationSer(data=Q_data)
        if serializer.is_valid():
            part_id = serializer.save()
            uid = part_id.id
        else:
            return serializer.errors

        # AboutyouNotification.objects.create(title=title, text=text, link=link, from_user=from_user, to_user=to_user,
        #                                     post=post.id, all_post=post, type=type)

        up_notifactions_count(to_user.id)
        data = {"id": post_id, "type": 1, "feedType": "", "noticeMsgType": 4, "from_user_name": from_user.username,
                "musicName": post.music_info.music_name}
        device = FCMDevice.objects.filter(user=to_user).first()
        device.send_message(data=data)

        # post_save.connect(create_A_handler, sender=AboutyouNotification)
        return True
    except User.DoesNotExist as e:
        return e


@app.task
def comment_msg(from_user_id, to_user_id, post_id):
    try:
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)
        post = AllSongMusic.objects.get(id=post_id)
        title = 'new comment'
        text = 'comment your post'
        type = 5
        link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(post.id)

        Q_data = QueryDict(mutable=True)
        Q_data['title'] = title
        Q_data['text'] = text
        Q_data['link'] = link
        Q_data['from_user'] = from_user.id
        Q_data['to_user'] = to_user.id
        Q_data['post'] = post_id
        Q_data['all_post'] = post.id
        Q_data['type'] = type
        serializer = Create_AboutyouNotificationSer(data=Q_data)
        if serializer.is_valid():
            part_id = serializer.save()
            uid = part_id.id
        else:
            return serializer.errors
        #
        # AboutyouNotification.objects.create(title=title, text=text, link=link, from_user=from_user, to_user=to_user,
        #                                     post=post.id, all_post=post, type=type)
        #


        up_notifactions_count(to_user.id)

        # user_id = to_user.id
        data = {"id": post_id, "type": 1, "feedType": "", "noticeMsgType": 5, "from_user_name": from_user.username,
                "musicName": post.music_info.music_name}
        device = FCMDevice.objects.filter(user=to_user).first()
        # token_is=device.registration_id
        device.send_message(data=data)

        # post_save.connect(create_A_handler,sender=AboutyouNotification)

        return True
    except User.DoesNotExist as e:
        return e


@app.task
def following_msg(from_user_id, to_user_id):
    try:

        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)
        title = 'new following'
        text = 'following you'
        type = 3
        # link = "http://127.0.0.1:8000/api/v1/music/allmusicdetail/{0}/".format(post.id)
        # AboutyouNotification.objects.create(title=title, text=text, from_user=from_user, to_user=to_user, type=type)
        Q_data = QueryDict(mutable=True)
        Q_data['title'] = title
        Q_data['text'] = text
        Q_data['from_user'] = from_user.id
        Q_data['to_user'] = to_user.id
        Q_data['type'] = type
        serializer = Create_AboutyouNotificationSer(data=Q_data)
        if serializer.is_valid():
            part_id = serializer.save()
            uid = part_id.id
        else:
            return serializer.errors

        up_notifactions_count(to_user.id)
        # post_save.connect(create_A_handler, sender=AboutyouNotification)
        data = {"id": from_user_id, "type": 1, "feedType": "", "noticeMsgType": 3, "from_user_name": from_user.username,
                "musicName": ""}
        # device = FCMDevice.objects.filter(id=to_user_id).first()

        device = FCMDevice.objects.filter(user=to_user).first()
        device.send_message(data=data)
        return True
    except User.DoesNotExist as e:
        return e

def my_followers_msg(from_user_id,action_id):
    """我的关注动态发送给我的粉丝"""

    followers = r(from_user_id).followers()

    if followers:
        followers_id_list = list(followers)
        try:
            user_list = User.objects.filter(id__in=followers_id_list)
            action_user = User.objects.get(id=action_id)
            from_user = User.objects.get(id=from_user_id)
            title = 'new following'
            text = 'following you'
            type = 3
            for to_user in user_list:
                Q_data = QueryDict(mutable=True)
                Q_data['title'] = title
                Q_data['text'] = text
                Q_data['from_user'] = from_user.id
                Q_data['action_user']=action_user.id
                Q_data['to_user'] = to_user.id
                Q_data['type'] = type
                serializer = Create_FollowerNotificationSerializer(data=Q_data)
                if serializer.is_valid():
                    part_id = serializer.save()
                    uid = part_id.id
                else:
                    return serializer.errors
                up_notifactions_count(to_user.id)
                # data = {"id": from_user_id, "type": 1, "feedType": "", "noticeMsgType": 3, "from_user_name": from_user.username,
                #     "musicName": ""}
        except:
            return False
    else:
        return None


def my_praise_msg(from_user_id, action_id, post_id):
    """我的赞动态发送给我的粉丝"""

    followers = r(from_user_id).followers()

    if followers:
        followers_id_list = list(followers)
        try:
            user_list = User.objects.filter(id__in=followers_id_list)
            action_user = User.objects.get(id=action_id)
            from_user = User.objects.get(id=from_user_id)
            post = AllSongMusic.objects.get(id=post_id)

            title = 'new praise'
            text = 'praise your post'
            type = 4
            link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(post.id)
            for to_user in user_list:
                Q_data = QueryDict(mutable=True)
                Q_data['title'] = title
                Q_data['text'] = text
                Q_data['link'] = link
                Q_data['from_user'] = from_user.id
                Q_data['action_user']=action_user.id
                Q_data['to_user'] = to_user.id
                Q_data['post'] = post_id
                Q_data['all_post'] = post.id
                Q_data['type'] = type
                serializer = Create_FollowerNotificationSerializer(data=Q_data)
                if serializer.is_valid():
                    part_id = serializer.save()
                    uid = part_id.id
                else:
                    return serializer.errors
                up_notifactions_count(to_user.id)

        except:
            return False
    else:
        return None

def part_out(var):
    response = client_lambda.invoke(
        FunctionName='part_one',
        InvocationType='RequestResponse',
        Payload=json.dumps(var))
    return response


def all_out(var):
    response = client_lambda.invoke(
        FunctionName='allchorus',
        InvocationType='RequestResponse',
        Payload=json.dumps(var))
    return response

def part_fir_lam(var):
    response = client_lambda.invoke(
        FunctionName='part_fir',
        InvocationType='RequestResponse',
        Payload=json.dumps(var))
    return response


def all_fir_lam(var):
    response = client_lambda.invoke(
        FunctionName='all_fir',
        InvocationType='RequestResponse',
        Payload=json.dumps(var))
    return response


def all_sec_lam(var):
    response = client_lambda.invoke(
        FunctionName='all_sec',
        InvocationType='RequestResponse',
        Payload=json.dumps(var))
    return response

@app.task
def music_lambda(data):
    aac_bucket_name = "duetin-android-upaac"  # 上传音频
    mp4_bucket_name = "duetin-android-upmp4"  # 上传视频
    banzou_bucket_name = "duetin-accompany"  # 伴奏文件
    jpg_bucket_name = "duetin-user-tx"  # 第一次唱合成的图片固定
    jpg_key_name = "jpg_out_test_20170811123400_23133.jpg"
    cuted_bucket_name = "duetin-cuted"  # 视频加处理好干声
    duetin_part_one_bucket = 'duetin-part-one'  # 合成后视频加伴奏加人声未拼接
    part_bucket_name = "duetin-part"  # 合成后视频bucket
    all_bucket_name = 'duetin-chorus'

    aac_key_name = data['aac_key_name']
    mp4_key_name = data["mp4_key_name"]
    user_id = data['user_id']
    invite = data['invite']
    title = data['title']
    part_to = data['part_to']  # 将要唱的part部分
    is_enable = data['is_enable']
    music_id = data['music_id']
    participant_id = data['participant_id']
    ts = data['ts']

    try:
        music_auth = User.objects.get(id=user_id)
        music_info = MusicProfiel.objects.get(pk=music_id)

    except User.DoesNotExist as e:
        return e

    username = music_auth.username

    banzou_bucket_key = music_info.bucket_accompany_key

    if participant_id < 1:
        part_fir = {
            "username": username,
            "mp4_bucket_name": mp4_bucket_name,
            "mp4_key_name": mp4_key_name,
            "aac_bucket_name": aac_bucket_name,
            "aac_key_name": aac_key_name,
            "banzou_bucket_name": banzou_bucket_name,
            "banzou_key_name": banzou_bucket_key,
            "jpg_bucket_name": jpg_bucket_name,
            "jpg_key_name": jpg_key_name,
            "cuted_bucket_name": cuted_bucket_name,
            "part_one_mp4_bucket_name": duetin_part_one_bucket
        }

        response_fir = part_fir_lam(part_fir)
        statuscode_fir = response_fir['StatusCode']
        if statuscode_fir == 200:
            try:
                payload = response_fir['Payload'].read().decode()
                res_data_u = json.JSONDecoder().decode(payload)
                res_data = json.loads(res_data_u)

                cuted_out_mp4 = res_data['cuted_out_mp4']
                part_one_mp4 = res_data['part_one_mp4']
                part_compose_mp4 = res_data['part_compose_mp4']
                part_compose_jpg = res_data['part_compose_jpg']
            except:
                return "lambda1 error"
        else:
            return "lambda1 code error"
        part_one_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part-one/" + part_one_mp4
        part_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/compose_vedio/" + part_compose_mp4
        part_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/out_jpg/" + part_compose_jpg

        Q_data = QueryDict(mutable=True)

        Q_data['title'] = title
        Q_data['music_info'] = music_info.id
        Q_data['music_auth'] = music_auth.id

        Q_data['vedio_bucket_name'] = mp4_bucket_name
        Q_data['vedio_bucket_key'] = mp4_key_name
        Q_data["aac_bucket_name"] = aac_bucket_name
        Q_data['aac_bucket_key'] = aac_key_name
        Q_data['cuted_bucket_name'] = cuted_bucket_name
        Q_data['cuted_bucket_key'] = cuted_out_mp4
        Q_data['one_bucket_name'] = duetin_part_one_bucket
        Q_data['one_bucket_key'] = part_one_mp4
        Q_data['part_vedio_bucket_name'] = part_bucket_name
        Q_data['part_vedio_key'] = "compose_vedio/" + part_compose_mp4
        Q_data['part_vedio_url'] = part_one_vedio_url
        Q_data['part'] = part_to
        Q_data['is_enable'] = is_enable

        # serializer = PartSoneSerializer(data={"title":title,"music_info":music_info,"music_auth":music_auth,"auth_photo":res_data['out_jpg'],"vedio_url":res_data['compose_vedio'],"socre":socre,"part":part,"is_enable":is_enable})
        serializer = CreatePartSongSerializer(data=Q_data)
        if serializer.is_valid():
            part_id = serializer.save()
            uid = part_id.id
        else:
            return serializer.errors

        Q_data['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
        Q_data['music_participant_part'] = None
        Q_data['all_music_auth'] = music_auth.id
        Q_data['vedio'] = part_vedio_url

        Q_data["bucket_all_vedio_name"] = part_bucket_name
        Q_data['bucket_all_vedio_key'] = "compose_vedio/" + part_compose_mp4
        Q_data['photo'] = part_jpg_url
        serializer_all = CreateAllSongMusicSerializer(data=Q_data)
        if serializer_all.is_valid():
            all_music = serializer_all.save()

            data = {"id": all_music.id, "type": 2, "feedType": "uploadComplete", "noticeMsgType": 0,
                    "from_user_name": music_auth.username,
                    "musicName": music_info.music_name, "ts": ts}
            device = FCMDevice.objects.filter(user=music_auth).first()
            device.send_message(data=data)

        else:
            return serializer.errors

        if invite:
            for i in invite:
                to_user_id = int(i)
                from_user = music_auth
                to_user = User.objects.get(pk=to_user_id)

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
                # device = FCMDevice.objects.filter(id=to_user_id).first()

                device = FCMDevice.objects.filter(user=to_user).first()
                device.send_message(data=data)
                # post_save.connect(create_N_handler, sender=Notification)

        return "ok"

    else:
        all_first = {
            "username": username,
            "mp4_bucket_name": mp4_bucket_name,
            "mp4_key_name": mp4_key_name,
            "aac_bucket_name": aac_bucket_name,
            "aac_key_name": aac_key_name,
            "banzou_bucket_name": banzou_bucket_name,
            "banzou_key_name": banzou_bucket_key,
            "cuted_bucket_name": cuted_bucket_name,
            "part_one_mp4_bucket_name": duetin_part_one_bucket
        }

        response_fir = all_fir_lam(all_first)
        statuscode_fir = response_fir['StatusCode']
        if statuscode_fir == 200:
            try:
                payload = response_fir['Payload'].read().decode()
                res_data_u = json.JSONDecoder().decode(payload)
                res_data = json.loads(res_data_u)

                cuted_out_mp4 = res_data['cuted_out_mp4']
                part_one_mp4 = res_data['part_one_mp4']

            except:
                return "lambda3 error"
        else:
            return "lambda3 code error"

        # part_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/compose_vedio/" + part_compose_mp4
        # part_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/out_jpg/" + part_compose_jpg

        Q_data_one = QueryDict(mutable=True)

        Q_data_one['title'] = title
        Q_data_one['music_info'] = music_info.id
        Q_data_one['music_auth'] = music_auth.id

        Q_data_one['vedio_bucket_name'] = mp4_bucket_name
        Q_data_one['vedio_bucket_key'] = mp4_key_name
        Q_data_one["aac_bucket_name"] = aac_bucket_name
        Q_data_one['aac_bucket_key'] = aac_key_name
        Q_data_one['cuted_bucket_name'] = cuted_bucket_name
        Q_data_one['cuted_bucket_key'] = cuted_out_mp4
        Q_data_one['one_bucket_name'] = duetin_part_one_bucket
        Q_data_one['one_bucket_key'] = part_one_mp4

        Q_data_one['part'] = part_to
        Q_data_one['is_enable'] = is_enable

        serializer = CreatePartSongSerializer(data=Q_data_one)
        if serializer.is_valid():
            part_id = serializer.save()
            uid = part_id.id
        else:
            return serializer.errors

        participant_music = PartSongMusic.objects.get(id=participant_id)

        participant_vedio_key = participant_music.one_bucket_key  # 视频加干声加伴奏
        mycut_vedio_key = cuted_out_mp4

        all_sec = {
            "username": username,
            "cuted_mp4": mycut_vedio_key,
            "compose_mp4": participant_vedio_key,
            "all_compose_bucket_name": all_bucket_name,
            "cuted_bucket_name": cuted_bucket_name,
            "part_one_mp4_bucket_name":duetin_part_one_bucket

        }

        response_all = all_sec_lam(all_sec)
        statuscode_all = response_all['StatusCode']
        if statuscode_all == 200:
            try:
                payload_all = response_all['Payload'].read().decode()
                res_data_all_u = json.JSONDecoder().decode(payload_all)
                res_all_data = json.loads(res_data_all_u)

                all_music_video_name = res_all_data['all_compose_mp4']
                out_all_jpg_name = res_all_data['all_compose_jpg']
            except:
                return "lambda2 error"
        else:
            return "lambda2 code error"

        all_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-chorus/compose_vedio/" + all_music_video_name
        all_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-chorus/out_jpg/" + out_all_jpg_name

        Q_data_all = QueryDict(mutable=True)
        Q_data_all['title'] = title
        Q_data_all['music_info'] = music_info.id
        # Q_data_all['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
        Q_data_all['music_auth_part'] = part_id.id

        Q_data_all['music_participant_part'] = participant_music.id
        Q_data_all['all_music_auth'] = music_auth.id
        Q_data_all['photo'] = all_jpg_url
        Q_data_all['vedio'] = all_vedio_url
        Q_data_all["bucket_all_vedio_name"] = all_bucket_name
        Q_data_all['bucket_all_vedio_key'] = "compose_vedio/" + all_music_video_name
        Q_data_all['is_enable'] = is_enable

        serializer_all = CreateAllSongMusicSerializer(data=Q_data_all)
        if serializer_all.is_valid():
            all_music = serializer_all.save()

            data = {"id": all_music.id, "type": 2, "feedType": "uploadComplete", "noticeMsgType": 0,
                    "from_user_name": music_auth.username,
                    "musicName": music_info.music_name, "ts": ts}
            device = FCMDevice.objects.filter(user=music_auth).first()
            device.send_message(data=data)

            # 加入视频
            join_title = "new join"
            join_text = "join your post"
            join_type = 2
            join_id = all_music.id
            join_to_user = participant_music.music_auth
            join_link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(join_id)

            Notification.objects.create(title=join_title, text=join_text, from_user=music_auth,
                                        to_user=join_to_user, type=join_type,
                                        link=join_link)

            data = {"id": all_music.id, "type": 1, "feedType": "", "noticeMsgType": 2,
                    "from_user_name": music_auth.username,
                    "musicName": music_info.music_name}
            # device = FCMDevice.objects.filter(id=to_user_id).first()

            device = FCMDevice.objects.filter(user=join_to_user).first()
            device.send_message(data=data)
            # post_save.connect(create_N_handler, sender=Notification)

        else:
            return serializer.errors
        if invite:
            for i in invite:
                to_user_id = int(i)
                from_user = music_auth
                to_user = User.objects.get(pk=to_user_id)

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
                # device = FCMDevice.objects.filter(id=to_user_id).first()

                device = FCMDevice.objects.filter(user=to_user).first()
                device.send_message(data=data)
                # post_save.connect(create_N_handler, sender=Notification)

        return "ok"

# @app.task
def music_lambda_old(data):
    aac_bucket_name = "duetin-android-upaac"  # 上传音频
    mp4_bucket_name = "duetin-android-upmp4"  # 上传视频
    banzou_bucket_name = "duetin-accompany"  # 伴奏文件
    jpg_bucket_name = "duetin-user-tx"  # 第一次唱合成的图片固定
    jpg_key_name = "jpg_out_test_20170811123400_23133.jpg"
    # p_mp4_bucket_name = "duetin-processing"  # 提取纯视频
    # p_aac_bucket_name = "duetin-pydub-voice"  # 上传处理后音频
    cuted_bucket_name = "duetin-cuted"  # 视频加处理好干声
    # duetin_hc_voice_bucket = "duetin-hc-voice"  # 合成干声加伴奏
    duetin_part_one_bucket = 'duetin-part-one'  # 合成后视频加伴奏加人声未拼接
    part_bucket_name = "duetin-part"  # 合成后视频bucket
    all_bucket_name = 'duetin-chorus'

    aac_key_name = data['aac_key_name']
    mp4_key_name = data["mp4_key_name"]

    # username = data['username']
    user_id = data['user_id']
    invite = data['invite']
    title = data['title']
    part_to = data['part_to']  # 将要唱的part部分
    is_enable = data['is_enable']
    music_id = data['music_id']
    participant_id = data['participant_id']
    ts = data['ts']


    try:
        music_auth = User.objects.get(id=user_id)
        music_info = MusicProfiel.objects.get(pk=music_id)

    except User.DoesNotExist as e:
        return e

    username = music_auth.username

    banzou_bucket_key = music_info.bucket_accompany_key

    part_var = {
        "username": username,
        "mp4_bucket_name": mp4_bucket_name,
        "mp4_key_name": mp4_key_name,
        "aac_bucket_name": aac_bucket_name,
        "aac_key_name": aac_key_name,
        "banzou_bucket_name": banzou_bucket_name,
        "banzou_key_name": banzou_bucket_key,
        "jpg_bucket_name": jpg_bucket_name,
        "jpg_key_name": jpg_key_name
    }



    response_sec = part_out(part_var)
    statuscode2 = response_sec['StatusCode']
    if statuscode2 == 200:
        try:
            payload = response_sec['Payload'].read().decode()
            res_data_u = json.JSONDecoder().decode(payload)
            res_data = json.loads(res_data_u)

            cuted_out_mp4=res_data['cuted_out_mp4']
            part_one_mp4=res_data['part_one_mp4']
            part_compose_mp4=res_data['part_compose_mp4']
            part_compose_jpg=res_data['part_compose_jpg']
        except:
            return "lambda1 error"
    else:
        return "lambda1 code error"
    part_one_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part-one/" + part_one_mp4

    part_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/" + part_compose_mp4
    part_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-part/" + part_compose_jpg

    Q_data = QueryDict(mutable=True)

    Q_data['title'] = title
    Q_data['music_info'] = music_info.id
    Q_data['music_auth'] = music_auth.id

    Q_data['vedio_bucket_name'] = mp4_bucket_name
    Q_data['vedio_bucket_key'] = mp4_key_name
    Q_data["aac_bucket_name"] = aac_bucket_name
    Q_data['aac_bucket_key'] = aac_key_name

    # Q_data['pydub_bucket_name'] = p_aac_bucket_name
    # Q_data['pydub_bucket_key'] = "pydub_voice_test_20170810123733_22278.mp3"

    # Q_data['hc_aac_bucket_name'] = duetin_hc_voice_bucket
    # Q_data['hc_aac_key_name'] = hc_aac_key

    Q_data['cuted_bucket_name'] = cuted_bucket_name
    Q_data['cuted_bucket_key'] = cuted_out_mp4
    Q_data['one_bucket_name']=duetin_part_one_bucket
    Q_data['one_bucket_key']=part_one_mp4
    Q_data['part_vedio_bucket_name'] = part_bucket_name
    Q_data['part_vedio_key'] =  part_compose_mp4
    Q_data['part_vedio_url'] = part_one_vedio_url
    Q_data['part'] = part_to
    Q_data['is_enable'] = is_enable

    # serializer = PartSoneSerializer(data={"title":title,"music_info":music_info,"music_auth":music_auth,"auth_photo":res_data['out_jpg'],"vedio_url":res_data['compose_vedio'],"socre":socre,"part":part,"is_enable":is_enable})
    serializer = CreatePartSongSerializer(data=Q_data)
    if serializer.is_valid():
        part_id = serializer.save()
        uid = part_id.id
    else:
        return serializer.errors

    if participant_id > 0:
        participant_music = PartSongMusic.objects.get(id=participant_id)
        # participant_bucket_name = participant_music.part_vedio_bucket_name

        participant_vedio_key = participant_music.one_bucket_key#视频加干声加伴奏
        mycut_vedio_key = cuted_out_mp4

        all_val = {
            "username": username,
            "cuted_mp4": mycut_vedio_key,
            "compose_mp4": participant_vedio_key
        }

        response_all = all_out(all_val)
        statuscode_all = response_all['StatusCode']
        if statuscode_all == 200:
            try:
                payload_all = response_all['Payload'].read().decode()
                res_data_all_u = json.JSONDecoder().decode(payload_all)
                res_all_data = json.loads(res_data_all_u)

                all_music_video_name = res_all_data['all_compose_mp4']
                out_all_jpg_name = res_all_data['all_compose_jpg']
            except:
                return "lambda2 error"
        else:
            return "lambda2 code error"

        all_vedio_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-chorus/compose_vedio/" + all_music_video_name
        all_jpg_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-chorus/out_jpg/" + out_all_jpg_name

        Q_data_all = QueryDict(mutable=True)
        Q_data_all['title'] = title
        Q_data_all['music_info'] = music_info.id
        Q_data_all['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
        Q_data_all['music_participant_part'] = participant_music.id
        Q_data_all['all_music_auth'] = music_auth.id
        Q_data_all['photo'] = all_jpg_url
        Q_data_all['vedio'] = all_vedio_url
        Q_data_all["bucket_all_vedio_name"] = all_bucket_name
        Q_data_all['bucket_all_vedio_key'] = "compose_vedio/" + all_music_video_name
        Q_data_all['is_enable'] = is_enable

        serializer_all = CreateAllSongMusicSerializer(data=Q_data_all)
        if serializer_all.is_valid():
            all_music = serializer_all.save()

            data = {"id": all_music.id, "type": 2, "feedType": "uploadComplete", "noticeMsgType": 0,
                    "from_user_name": music_auth.username,
                    "musicName": music_info.music_name, "ts": ts}
            device = FCMDevice.objects.filter(user=music_auth).first()
            device.send_message(data=data)

            # 加入视频
            join_title = "new join"
            join_text = "join your post"
            join_type = 2
            join_id = all_music.id
            join_to_user = participant_music.music_auth
            join_link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(join_id)

            Notification.objects.create(title=join_title, text=join_text, from_user=music_auth,
                                        to_user=join_to_user, type=join_type,
                                        link=join_link)

            data = {"id": all_music.id, "type": 1, "feedType": "", "noticeMsgType": 2,
                    "from_user_name": music_auth.username,
                    "musicName": music_info.music_name}
            # device = FCMDevice.objects.filter(id=to_user_id).first()

            device = FCMDevice.objects.filter(user=join_to_user).first()
            device.send_message(data=data)
            # post_save.connect(create_N_handler, sender=Notification)

        else:
            return serializer.errors
        if invite:
            for i in invite:
                to_user_id = int(i)
                from_user = music_auth
                to_user = User.objects.get(pk=to_user_id)

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
                # device = FCMDevice.objects.filter(id=to_user_id).first()

                device = FCMDevice.objects.filter(user=to_user).first()
                device.send_message(data=data)
                # post_save.connect(create_N_handler, sender=Notification)

        return "ok"


    else:
        Q_data['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
        Q_data['music_participant_part'] = None
        Q_data['all_music_auth'] = music_auth.id
        Q_data['vedio'] = part_vedio_url

        Q_data["bucket_all_vedio_name"] = part_bucket_name
        Q_data['bucket_all_vedio_key'] = "compose_vedio/" + part_compose_mp4
        Q_data['photo'] = part_jpg_url
        serializer_all = CreateAllSongMusicSerializer(data=Q_data)
        if serializer_all.is_valid():
            all_music = serializer_all.save()

            data = {"id": all_music.id, "type": 2, "feedType": "uploadComplete", "noticeMsgType": 0, "from_user_name": music_auth.username,
                    "musicName": music_info.music_name,"ts":ts}
            device = FCMDevice.objects.filter(user=music_auth).first()
            device.send_message(data=data)

        else:
            return serializer.errors

        if invite:
            for i in invite:
                to_user_id = int(i)
                from_user = music_auth
                to_user = User.objects.get(pk=to_user_id)

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
                # device = FCMDevice.objects.filter(id=to_user_id).first()

                device = FCMDevice.objects.filter(user=to_user).first()
                device.send_message(data=data)
                # post_save.connect(create_N_handler, sender=Notification)

        return "ok"


def music_lambda1(data):
    bucket_name = data.get("bucket_name", "duetin-android-upfile")
    down_key = data.get("down_key", '')
    user_id = data.get('user_id', "")
    invite = data.get('invite', "")
    title = data.get('title', "")
    part_to = data.get('part_to', "")  # 将要唱的part部分
    is_enable = data.get('is_enable')
    # socre = data.get('socre', "")
    music_id = data.get('music_id', "")
    participant_id = data.get('participant_id', 0)

    try:
        music_auth = User.objects.get(id=user_id)
        music_info = MusicProfiel.objects.get(pk=music_id)

    except User.DoesNotExist as e:
        return e

    username = music_auth.username

    # banzou_url = music_info.accompany
    banzou_bucket_name = music_info.bucket_accompany_name
    banzou_bucket_key = music_info.bucket_accompany_key

    import boto3
    # client = boto3.client('lambda',
    #                       region_name="ap-southeast-1",
    #                       aws_access_key_id="AKIAIE665KY6G6OJARGA",
    #                       aws_secret_access_key="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")
    bucket_name_andriod = "duetin-android-upfile"
    var = {

        "username": username,
        "bucket_name": bucket_name_andriod,
        "down_key": down_key,
        "banzou_bucket_name": banzou_bucket_name,
        "banzou_bucket_key": banzou_bucket_key

        # "url": "http://duetin-shangchuan.oss-cn-shanghai.aliyuncs.com/zuixin1.mp4",
        # "banzou": "http://testduetin-accompany.oss-cn-shanghai.aliyuncs.com/1_2.aac"
        # "url": mp4_url,
        # "banzou": banzou_url
    }

    Q_data = QueryDict(mutable=True)
    is_ok = True
    i = 1
    part_vedio_url = ""
    caijian_vedio_url = ""
    part_jpg_url = ''
    while is_ok:
        response = part_out(var)
        statuscode = response['StatusCode']
        if statuscode == 200:
            try:
                payload = response['Payload'].read().decode()
                res_data_u = json.JSONDecoder().decode(payload)
                res_data = json.loads(res_data_u)

                caijian_vedio_url = res_data["caijian_vedio_url"]
                part_vedio_url = res_data["part_vedio_url"]
                part_jpg_url = res_data["part_jpg_url"]

                is_ok = False
            except:
                i = i + 1
                if i < 4:
                    is_ok = True
                else:
                    is_ok = False
        else:
            i = i + 1
            if i < 4:
                is_ok = True
            else:
                is_ok = False
    if caijian_vedio_url:
        url_list1 = caijian_vedio_url.split('/')
        caijian_name = url_list1[-1]
    else:
        return None
    if part_vedio_url:
        url_list2 = part_vedio_url.split('/')
        part_video_name = url_list2[-1]
    else:
        return None
    if part_jpg_url:
        url_list3 = part_jpg_url.split('/')
        part_jpg_name = url_list3[-1]
    else:
        return None

    Q_data['title'] = title
    Q_data['music_info'] = music_info.id
    Q_data['music_auth'] = music_auth.id

    Q_data['auth_photo'] = part_jpg_url
    Q_data['bucket_part_photo_name'] = "duetin-part"
    Q_data['bucket_part_photo_key'] = "out_jpg/" + part_jpg_name
    Q_data['auth_vedio'] = caijian_vedio_url
    Q_data['bucket_caivedio_name'] = "duetin-cuted"
    Q_data['bucket_caivedio_key'] = caijian_name
    Q_data['vedio_url'] = part_vedio_url
    Q_data['bucket_part_vedio_name'] = "duetin-part"
    Q_data['bucket_part_vedio_key'] = "compose_vedio/" + part_video_name

    # Q_data['socre'] = socre
    Q_data['part'] = part_to
    Q_data['is_enable'] = is_enable

    # serializer = PartSoneSerializer(data={"title":title,"music_info":music_info,"music_auth":music_auth,"auth_photo":res_data['out_jpg'],"vedio_url":res_data['compose_vedio'],"socre":socre,"part":part,"is_enable":is_enable})
    serializer = CreatePartSongSerializer(data=Q_data)
    if serializer.is_valid():
        # xxx = serializer.validated_data
        part_id = serializer.save()
        uid = part_id.id
    else:
        return serializer.errors

    if participant_id > 0:
        participant_music = PartSongMusic.objects.get(id=participant_id)
        participant_bucket_name = participant_music.bucket_part_vedio_name

        participant_vedio_key = participant_music.bucket_part_vedio_key
        my_bucket_name = "duetin-cuted"
        my_vedio_key = caijian_name
        is_all_ok = True
        all_vedio_url = ""
        all_jpg_url = ""
        while is_all_ok:

            all_val = {
                "username": username,
                "participant_bucket_name": participant_bucket_name,
                "participant_vedio_key": participant_vedio_key,
                "my_bucket_name": my_bucket_name,
                "my_vedio_key": my_vedio_key

            }
            response_all = all_out(all_val)
            statuscode_all = response_all['StatusCode']
            # statuscode=200
            if statuscode_all == 200:
                try:
                    payload_all = response_all['Payload'].read().decode()
                    res_data_all_u = json.JSONDecoder().decode(payload_all)
                    res_all_data = json.loads(res_data_all_u)

                    all_vedio_url = res_all_data['all_vedio_url']
                    all_jpg_url = res_all_data['all_jpg_url']

                    is_all_ok = False
                except:
                    i = i + 1
                    if i < 4:
                        is_all_ok = True
                    else:
                        is_all_ok = False
        if all_vedio_url:
            url_list_all_vedio = all_vedio_url.split('/')
            allvideo_name = url_list_all_vedio[-1]
        else:
            return None
        if all_jpg_url:
            url_list_all_jpg = all_jpg_url.split('/')
            alljpg_name = url_list_all_jpg[-1]
        else:
            return None
        Q_data_all = QueryDict(mutable=True)
        Q_data_all['title'] = title
        Q_data_all['music_info'] = music_info.id
        Q_data_all['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
        Q_data_all['music_participant_part'] = participant_music.id
        Q_data_all['all_music_auth'] = music_auth.id
        Q_data_all['photo'] = all_jpg_url
        Q_data_all['bucket_all_photo_name'] = "duetin-chorus"
        Q_data_all['bucket_all_photo_key'] = "out_jpg/" + alljpg_name
        Q_data_all['vedio'] = all_vedio_url
        Q_data_all["bucket_all_vedio_name"] = "duetin-chorus"
        Q_data_all['bucket_all_vedio_key'] = "compose_vedio/" + allvideo_name
        Q_data_all['is_enable'] = is_enable

        serializer_all = CreateAllSongMusicSerializer(data=Q_data_all)
        if serializer_all.is_valid():
            all_music = serializer_all.save()
            if invite:
                for i in invite:
                    to_user_id = int(i)
                    from_user = music_auth
                    to_user = User.objects.get(pk=to_user_id)

                    title = 'new invite'
                    text = 'invite your join'
                    type = 0
                    post_id = all_music.id
                    link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(post_id)
                    Notification.objects.create(title=title, text=text, from_user=from_user,
                                                to_user=to_user, type=type,
                                                link=link)
                    up_notifactions_count(to_user_id)
        else:
            return serializer.errors
    else:
        Q_data['music_auth_part'] = PartSongMusic.objects.get(id=uid).id
        Q_data['music_participant_part'] = None
        Q_data['all_music_auth'] = music_auth.id
        Q_data['vedio'] = part_vedio_url
        Q_data['bucket_all_photo_name'] = "duetin-part"
        Q_data['bucket_all_photo_key'] = "out_jpg/" + part_jpg_name
        Q_data["bucket_all_vedio_name"] = "duetin-part"
        Q_data['bucket_all_vedio_key'] = "compose_vedio/" + part_video_name
        Q_data['photo'] = part_jpg_url
        serializer_all = CreateAllSongMusicSerializer(data=Q_data)
        if serializer_all.is_valid():
            all_music = serializer_all.save()
        else:
            return serializer.errors

        if invite:
            for i in invite:
                to_user_id = int(i)
                from_user = music_auth
                to_user = User.objects.get(pk=to_user_id)

                title = 'new invite'
                text = 'invite your join'
                type = 0
                post_id = all_music.id
                link = "http://duetin.com/api/v1/music/allmusicdetail/{0}/".format(post_id)
                Notification.objects.create(title=title, text=text, from_user=from_user,
                                            to_user=to_user, type=type,
                                            link=link)
                up_notifactions_count(to_user_id)

    return True

@app.task
def up_to_aws(data):
    post_url = "http://duetin.xin/uptoaws/"
    if data:
        aac_key_name = data['aac_key_name']
        mp4_key_name = data['mp4_key_name']
        up_data = {"aac_file": aac_key_name, "mp4_file": mp4_key_name}

        try:
            token = 'Token b969103ac191c25fa31f7fc5505812286536b582'
            headers = {'content-type': 'application/json', 'Authorization': token}

            r = requests.post(url=post_url, json=up_data, headers=headers)
            msg = r.text

        except Exception, e:

            pass
        con_linux(data)

        return "ok"

    else:
        return "not data"


def con_linux(data):
    import sys
    # aac_bucket_name = "duetin-android-upaac"  # 上传音频
    # mp4_bucket_name = "duetin-android-upmp4"  # 上传视频
    # banzou_bucket_name = "duetin-accompany"  # 伴奏文件
    # jpg_bucket_name = "duetin-user-tx"  # 第一次唱合成的图片固定
    # jpg_key_name = "jpg_out_test_20170811123400_23133.jpg"
    # cuted_bucket_name = "duetin-cuted"  # 视频加处理好干声
    # duetin_part_one_bucket = 'duetin-part-one'  # 合成后视频加伴奏加人声未拼接
    # part_bucket_name = "duetin-part"  # 合成后视频bucket
    # all_bucket_name = 'duetin-chorus'
    #
    # aac_key_name = data['aac_key_name']
    # mp4_key_name = data["mp4_key_name"]
    # user_id = data['user_id']
    # invite = data['invite']
    # title = data['title']
    # part_to = data['part_to']  # 将要唱的part部分
    # is_enable = data['is_enable']
    # music_id = data['music_id']
    # participant_id = data['participant_id']
    # ts = data['ts']

    # con_data = {"aac_bucket_name": aac_bucket_name, "mp4_bucket_name": mp4_bucket_name,
    #             "banzou_bucket_name": banzou_bucket_name}
    PORT = 10180
    import socket

    sock_data = "jsonfile*" + json.dumps(data)


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(('172.31.17.161', PORT))
        s.sendall('A01' + sock_data + '\n=====\n')
        s.close()
    except socket.error, e:
    # print e
        return "error"
    return "ok"


    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try:
    #     sock.connect(('172.31.29.123', 8001))
    #
    # except:
    #     print "connect error"
    #     sys.exit()
    # print 'dic type ', type(con_data)
    # st = json.dumps(con_data)
    # print 'after dumps ', type(st)
    # ss=sock.send(st)

    # response = sock.recv(1024)
    # print("recv " + response);
    # sock.close()