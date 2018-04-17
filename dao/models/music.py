# -*- coding: utf-8 -*-

"""
Create at 2017/3/21
歌曲数据模型
"""
from __future__ import unicode_literals
from django.db.models import CharField, BooleanField, PositiveSmallIntegerField, \
    IntegerField, Model
from django.db import models
# from django.contrib.auth.models import User
from app_auth.models import User

# Create your models here.
SEX_TYPE = (
    (0, 'MAN'),
    (1, 'women'),
)

LANGUAGE_TYPE = (
    (0, 'CHN'),
    (1, 'ENG'),
)

MUSIC_STYLE = (
    (0, 'MELODY'),
    (1, 'RAP'),
    (2, 'Rap&Melody'),
    (9, 'Undefined'),
)

PEITAIN_TO = (
    (0, 'PART_A'),
    (1, 'PART_B'),
)

REPORT_SONG_TYPE = (
    (0, 'Music Quality'),
    (1, 'Lyric Quality'),
    (2, 'Partner Complaint'),
)

NOTIFICATION_TYPE = (
    (1, 'JOIN'),
    (2, 'INVITED'),
)
ABOUTNOTIFICATION_TYPE = (
    (3, 'FOLLOWING'),
    (4, 'LIKE'),
    (5, 'COMMENT'),
)

RATING_SCALE = (
    (1, 'A'),
    (2, 'B'),
    (3, 'C'),
    (4, 'D'),
    (5, 'E'),

)


class AllMusicCategory(models.Model):
    """
    All music分类表
    """
    name = models.CharField(max_length=200, verbose_name=u'类别名称')
    id_name=models.CharField(max_length=200,blank=True,null=True, verbose_name=u'印尼类别名称')
    rank = models.IntegerField(default=0, verbose_name=u'排序')
    is_online = models.BooleanField(default=True, verbose_name=u'是否显示')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        ordering = ['-rank']
        verbose_name_plural = u'合成歌曲分类管理'

    def __str__(self):
        return self.name


class Singer(Model):
    """歌手表"""
    singer_name = CharField(max_length=200, verbose_name=u'歌手名')
    uid = CharField(max_length=255, unique=True, verbose_name=u'上传数据唯一标识')
    singer_country = CharField(max_length=200, blank=True, null=True, verbose_name=u'所属国家')
    sex = IntegerField(choices=SEX_TYPE, blank=True, null=True, verbose_name=u'性别')
    rank = IntegerField(default=0, verbose_name=u'排序')
    photo = CharField(max_length=200, blank=True, null=True, verbose_name=u'歌手图片')
    singer_ico = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'歌手头像')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural = u'歌手管理'
        ordering = ['-rank']

    def __str__(self):
        return self.singer_name


class MusicProfiel(Model):
    """歌曲信息表"""

    music_name = CharField(max_length=200, blank=True, null=True, verbose_name=u'歌曲名')
    uid = models.CharField(max_length=200, blank=True, null=True, unique=True, verbose_name=u'歌曲唯一标识')
    singer = models.ManyToManyField(Singer, related_name='singer_info', db_index=True)
    language = IntegerField(choices=LANGUAGE_TYPE, blank=True, null=True, verbose_name=u'语言')
    Original_file = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'原唱音频文件')
    bucket_original_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'原唱文件BUCKET名称')
    bucket_original_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'原唱文件bucket的key')

    bucket_accompany_name = models.CharField(max_length=200, default="duetin-accompany", verbose_name=u'伴奏文件BUCKET名称')
    bucket_accompany_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'伴奏文件bucket的key')

    accompany = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'伴奏文件')
    # accompany_mp4 = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'MP4伴奏文件')
    # bucket_accompany_mp4_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'mp4伴奏文件BUCKET名称')
    # bucket_accompany_mp4_key = models.CharField(max_length=200, blank=True, null=True,
    #                                             verbose_name=u'mp4伴奏文件bucket的key')

    k_game = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'打分文件')
    lyrics = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'歌词文件')
    bucket_lyrics_name = models.CharField(max_length=200, default='duetin-lyrics', verbose_name=u'歌词文件BUCKET名称')
    bucket_lyrics_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'歌词文件bucket的key')
    segments = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'转场json文件')
    segments_bucket_name = models.CharField(max_length=200, default='duetin-segments', verbose_name=u'转场文件BUCKET名称')
    segments_key_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'转场文件bucket的key')

    image = models.CharField(blank=True, null=True, max_length=200, verbose_name=u'歌曲封面图片')
    bucket_image_name = models.CharField(max_length=200, default='duetin-music-image', verbose_name=u'歌曲图片文件BUCKET名称')
    bucket_image_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'歌曲图片文件bucket的key')

    style = models.IntegerField(choices=MUSIC_STYLE, blank=True, null=True, verbose_name=u'歌曲类型')
    is_loved = models.BooleanField(default=False, verbose_name=u'是否男女合唱')
    time_a = models.IntegerField(default=0, verbose_name=u'歌曲A开始唱的时间点')
    time_b = models.IntegerField(default=0, verbose_name=u'歌曲B开始唱的时间点')
    # mark_pic = models.CharField(max_length=200, verbose_name=u'打分缩略图')
    view_count = models.BigIntegerField(default=0, verbose_name=u'点击次数')
    sing_count = models.BigIntegerField(default=0, verbose_name=u'被合唱次数')
    rank = models.IntegerField(default=0, verbose_name=u'热度排序')
    new_sort = models.IntegerField(default=0, verbose_name=u'NEW页面手动排序')
    top_rank = models.IntegerField(default=0, verbose_name=u'top50排序')
    sort = models.IntegerField(default=0, verbose_name=u'手动排序')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')
    is_online = models.BooleanField(default=False, verbose_name=u'是否上线')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = u'歌曲信息关系'
        # ordering = ['-rank']

    def __str__(self):
        return self.music_name


class PartSongMusic(models.Model):
    """唱半首歌数据表"""
    title = models.CharField(max_length=200, verbose_name=u'标题', blank=True, null=True)
    music_info = models.ForeignKey(MusicProfiel, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='music_part',
                                   db_index=True,
                                   verbose_name=u'歌曲数据')
    music_auth = models.ForeignKey(User, related_name='my_part_post', db_index=True, verbose_name=u'发布人')
    vedio_bucket_name = models.CharField(max_length=200, default='duetin-android-upmp4', verbose_name=u'上传的原始视频bucket')
    vedio_bucket_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'上传的原始视频key')
    aac_bucket_name = models.CharField(max_length=200, default='duetin-android-upaac', verbose_name=u'上传的原始音频bucket')
    aac_bucket_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'上传的原始音频key')

    pydub_bucket_name = models.CharField(max_length=200, default='duetin-processing', verbose_name=u'调整后音频bucket')
    pydub_bucket_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'调整后音频key')

    hc_aac_bucket_name = models.CharField(max_length=200, default='duetin-hc-voice', verbose_name=u'音频伴奏合成后bucket')
    hc_aac_key_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'音频伴奏合成后key')

    cuted_bucket_name = models.CharField(max_length=200, default='duetin-cuted', verbose_name=u'视频干声合成后视频bucket')
    cuted_bucket_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'视频干声合成后视频key')

    one_bucket_name = models.CharField(max_length=200, default='duetin-part-one', verbose_name=u'视频伴奏干声合成后视频bucket')
    one_bucket_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'视频伴奏干声合成后视频key')

    one_gif_bucket = models.CharField(max_length=200, default='duetin-one-gif', verbose_name=u'part部分gif图片bucket')
    one_gif_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'part部分gif图片key')
    part_gif_url = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'GIF图片地址')

    one_jpg_bucket = models.CharField(max_length=200, default='duetin-one-jpg', verbose_name=u'part部分jpg图片bucket')
    one_jpg_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'part部分jpg图片key')

    part_user_img_key = models.CharField(max_length=200, default="part_user_img.jpg", blank=True, null=True,
                                         verbose_name=u'无视频合成图片key')
    part_user_img_bucket = models.CharField(max_length=200, default="duetin-android-image", blank=True, null=True,
                                            verbose_name=u'无视频合成图片bucket')

    part_vedio_bucket_name = models.CharField(max_length=200, default='duetin-part', verbose_name=u'合成视频文件BUCKET名称')
    part_vedio_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'合成视频文件bucket的key')
    part_vedio_url = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'视频地址')
    socre = models.IntegerField(default=100, verbose_name=u'得分')

    part = models.IntegerField(choices=PEITAIN_TO, blank=True, null=True, verbose_name=u'属于歌曲哪半部分')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    rating_scale = models.IntegerField(choices=RATING_SCALE, blank=True, null=True, verbose_name=u'评分等级')
    photo = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'显示图片地址')
    vedio = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'合成后视频地址')
    is_enable = models.BooleanField(default=True, verbose_name=u'是否可以加入')
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = u'半首歌数据管理'

    def __str__(self):
        return self.title


class PartComment(models.Model):
    """半部歌曲评论"""
    music = models.ForeignKey(PartSongMusic, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='part_music_comment', db_index=True, verbose_name=u'所属视频')
    content = models.TextField(verbose_name=u'评论内容')
    user = models.ForeignKey(User, related_name='partcomment_user', db_index=True, verbose_name=u'评论人')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'父级评论')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = u'半首歌评论管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.content


# @counters.add('hits')
class AllSongMusic(models.Model):
    """合唱完成表
        歌曲部分发起者为被匹配者，参与者为发布视频者
    """

    title = models.CharField(max_length=200, verbose_name=u'标题', blank=True, null=True)
    music_info = models.ForeignKey(MusicProfiel, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='music_pro', db_index=True, verbose_name=u'歌曲信息')
    music_auth_part = models.ForeignKey(PartSongMusic, blank=True, null=True, on_delete=models.SET_NULL,
                                        related_name='auth_music_part', db_index=True, verbose_name=u'发布歌曲者部分右边')
    music_participant_part = models.ForeignKey(PartSongMusic, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name='participant_music_part', db_index=True,
                                               verbose_name=u'参与者歌曲部分左边')
    all_music_auth = models.ForeignKey(User, related_name='my_all_post', db_index=True, verbose_name=u'发布人')
    all_gif_bucket = models.CharField(max_length=200, default='duetin-all-gif', verbose_name=u'all部分gif图片bucket')
    all_gif_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'all部分gif图片key')
    all_gif_url = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'GIF图片地址')
    share_jpg_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'share图片key')

    photo = models.CharField(max_length=200, verbose_name=u'显示图片地址')
    photo_key_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'合成图片的key')

    vedio = models.CharField(max_length=200, verbose_name=u'合成后视频地址')
    bucket_all_vedio_name = models.CharField(max_length=200, default='duetin-chorus', verbose_name=u'合成视频文件BUCKET名称')
    bucket_all_vedio_key = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'合成视频文件bucket的key')
    praise = models.BigIntegerField(default=0, verbose_name=u'被赞次数')
    view_count = models.BigIntegerField(default=0, verbose_name=u'观看次数')
    share_count = models.BigIntegerField(default=0, verbose_name=u'分享次数')
    rank = models.IntegerField(default=0, verbose_name=u'手动排序')
    rating_scale = models.IntegerField(choices=RATING_SCALE, blank=True, null=True, verbose_name=u'评分等级')
    hour_count = models.BigIntegerField(default=0, verbose_name=u'每小时观看次数')
    view_count_rank = models.FloatField(default=0, verbose_name=u'热门排序')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_enable = models.BooleanField(default=True, verbose_name=u'是否可以加入')
    is_delete = models.BooleanField(default=False)
    is_recommend_rank = models.IntegerField(default=0, verbose_name=u'推荐给新用户排序')
    all_category = models.ForeignKey(AllMusicCategory, related_name='all_category_video', blank=True, null=True,
                                     db_index=True,verbose_name=u'分类')

    class Meta:
        # ordering = ['-rank', '-view_count_rank','-created_at']
        verbose_name_plural = u'合唱歌曲数据管理'

    def __str__(self):
        return self.title


class ALLMusicPraise(models.Model):
    """赞过的用户"""
    music = models.ForeignKey(AllSongMusic, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='allmusic_praise', verbose_name=u'所属歌曲')
    owner = models.ForeignKey(User, related_name='parise_user', db_index=True, verbose_name=u'赞的人')
    # is_praise = models.BooleanField(blank=True, null=True,verbose_name=u'是否赞过')
    update_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = u'合唱歌曲点赞管理'

    def __str__(self):
        return self.is_praise


class ALLComment(models.Model):
    """合唱完成歌曲评论"""
    music = models.ForeignKey(AllSongMusic, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='all_music_comment', db_index=True, verbose_name=u'所属视频')
    text = models.CharField(max_length=250, verbose_name=u'评论内容')
    owner = models.ForeignKey(User, related_name='comment_user', blank=True, null=True, on_delete=models.SET_NULL,
                              verbose_name=u'评论人')
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=u'父级评论')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = u'合唱歌曲评论管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.text


class ReportSong(models.Model):
    """举报歌曲"""
    report_type = IntegerField(choices=REPORT_SONG_TYPE, blank=True, null=True, verbose_name=u'错误类型')
    report_music = models.ForeignKey(MusicProfiel, blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='report_music', verbose_name=u'举报的歌曲')
    is_solve = models.BooleanField(default=False, verbose_name=u'是否处理完毕')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = u'歌曲举报管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.report_type


class Notification(models.Model):
    """
    消息模型
    """
    title = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'标题')
    text = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'内容')
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'链接')
    from_user = models.ForeignKey(User, default=None, blank=True, null=True, related_name='from_user_notifaction',
                                  verbose_name=u'发送者')
    # action_user=models.ForeignKey(User, default=None, blank=True, null=True, related_name='action_user_notifaction',
    #                               verbose_name=u'被执行活动的人')
    post = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'相关作品ID')
    all_post = models.ForeignKey(AllSongMusic, blank=True, null=True, related_name='allsong_music_notifaction',
                                 verbose_name=u'相关作品')
    to_user = models.ForeignKey(User, related_name='to_user_notifaction', verbose_name=u'接受者')
    type = IntegerField(choices=NOTIFICATION_TYPE, blank=True, null=True, verbose_name=u'消息类型')
    is_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = u'消息管理'
        ordering = ('-created_at',)

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.created_at, now)

    def __str__(self):
        return self.title


class AboutyouNotification(models.Model):
    # 我的关注者的动态
    title = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'标题')
    text = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'内容')
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'链接')
    from_user = models.ForeignKey(User, default=None, blank=True, null=True, related_name='from_user_y_notifaction',
                                  verbose_name=u'发送者')
    action_user = models.ForeignKey(User, default=None, blank=True, null=True, related_name='action_user_y_notifaction',
                                    verbose_name=u'被执行活动的人')
    post = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'相关作品ID')
    all_post = models.ForeignKey(AllSongMusic, blank=True, null=True, related_name='music_y_notifaction',
                                 verbose_name=u'相关作品')
    to_user = models.ForeignKey(User, related_name='to_user_y_notifaction', verbose_name=u'接受消息者')
    type = IntegerField(choices=ABOUTNOTIFICATION_TYPE, blank=True, null=True, verbose_name=u'消息类型')
    is_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = u'关于你消息管理'
        ordering = ('-created_at',)

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.created_at, now)

    def __str__(self):
        return self.title
