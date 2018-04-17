# -*- coding: utf-8 -*-

"""
Create at 2017/3/21
这里做一个base model 其他model都集成base model
"""

__author__ = 'TT'

from django.db.models import Model, DateTimeField, BooleanField, IntegerField
from django.db import models
from app_auth.models import User
CASE_TYPE = (
    (1, 'Cannot find song'),
    (2, 'Wrong research result'),
)

class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'标题')
    content = models.TextField(blank=True, null=True, verbose_name=u'介绍说明')
    img = models.CharField(max_length=300, default='banner/default.jpg', verbose_name=u'图片地址')
    link = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'超链接')
    rank = models.IntegerField(default=0, verbose_name=u'手动排序')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=u'新建时间')
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = u'BANNER管理'

    def __str__(self):
        return self.title


class PostData(models.Model):
    uid = models.CharField(max_length=250, blank=True, null=True, verbose_name=u'执行iD')
    user_id = models.BigIntegerField(verbose_name=u'用户ID')
    username = models.CharField(max_length=100, verbose_name=u'用户名')

    title = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'标题')
    music_id = models.BigIntegerField(verbose_name=u'歌曲ID')
    participant_id = models.BigIntegerField(blank=True, null=True, verbose_name=u'对唱部分partID')
    part_to = models.BigIntegerField(verbose_name=u'要唱的部分0或者1')
    is_enable = models.BigIntegerField(default=1, verbose_name=u'是否允许加入')
    ts = models.BigIntegerField(verbose_name=u'TS值')
    trim = IntegerField(verbose_name=u'需要截取的时间')
    reverberation_type = models.IntegerField(default=0, verbose_name=u'混响效果')
    bmp_ts = models.IntegerField(default=8, verbose_name=u'截图时间点秒')

    invite = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'邀请列表')
    aac_key_name = models.CharField(max_length=300, verbose_name=u'音频key')
    mp4_key_name = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'视频KEY')
    banzou_key_name = models.CharField(max_length=300, verbose_name=u'伴奏key')
    participant_part_one_mp4 = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'合唱one视频key')
    part_jpg_key_name = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'第一次唱静态图片key')

    is_ok = models.BooleanField(default=False, verbose_name=u'是否执行成功')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=u'创建时间')
    complate_at = models.DateTimeField(null=True, blank=True, verbose_name=u'执行完毕时间')
    all_music_id = models.IntegerField(blank=True, null=True, verbose_name=u'作品ID')
    all_music_image = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'作品GIF')
    # reverberation=models.IntegerField(default=0,verbose_name=u'混响效果')
    # part_id=models.IntegerField(null=True,blank=True,verbose_name=u'PART部分ID')
    old_part = models.IntegerField(null=True, blank=True, verbose_name=u'旧的PART部分ID')
    old_participant = models.IntegerField(null=True, blank=True, verbose_name=u'旧的participant部分ID')

    class Meta:
        verbose_name_plural = u'合成任务管理'

    def __str__(self):
        return self.id


class ExceptionCase(models.Model):
    case_context = models.TextField(verbose_name=u'异常具体')
    case_user = models.ForeignKey(User, verbose_name=u'异常用户')
    case_type = models.IntegerField(default=0, verbose_name=u'异常类型')
    case_level = models.IntegerField(default=0, verbose_name=u'异常程度')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural = u'异常管理'

    def __str__(self):
        return self.case_level


class SongException(models.Model):
    song_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'歌曲名')
    singer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'歌手名')
    case_option = models.IntegerField(choices=CASE_TYPE, blank=True, null=True, verbose_name=u'问题类型')
    description = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'问题描述')
    is_settle = models.BooleanField(default=False, verbose_name=u'是否处理')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural = u'搜索歌曲异常管理'

    def __str__(self):
        return self.song_name


# class MobileVersion(models.Model):
#     mobile_brand=models.CharField(max_length=300,verbose_name=u'手机品牌')
#     mobile_name=models.CharField(max_length=300,verbose_name=u'手机名称')
#     mobile_version=models.CharField(max_length=300,verbose_name=u'手机型号')
#     mobile_edition=models.CharField(max_length=300,verbose_name=u'手机固件版本')
#     mobile_yj_name=models.CharField(max_length=300,verbose_name=u'硬件名称')
#     default_time=models.IntegerField(default=0,verbose_name=u'默认延迟毫秒数')
#     delay_time=models.IntegerField(default=0,verbose_name=u'延迟毫秒数')
#
#     class Meta:
#         verbose_name_plural=u'手机型号版本'
#
#     def __str__(self):
#         return self.mobile_brand



class OperationLogs(models.Model):
    object_id = models.IntegerField(blank=True, null=True, verbose_name=u'对象ID')
    object_rep = models.CharField(blank=True, null=True, max_length=300, verbose_name=u'对象名')
    type = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'类型')
    change_message = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'操作详情')
    user = models.ForeignKey(User, verbose_name=u'操作人')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural = u'用户操作日志'

    def __str__(self):
        return self.change_message
