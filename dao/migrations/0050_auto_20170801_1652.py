# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-01 08:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0049_musicprofiel_accompany_mp4'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musicprofiel',
            name='accompany_mp4',
        ),
        migrations.RemoveField(
            model_name='musicprofiel',
            name='bucket_accompany_mp4_key',
        ),
        migrations.RemoveField(
            model_name='musicprofiel',
            name='bucket_accompany_mp4_name',
        ),
        migrations.AlterField(
            model_name='allsongmusic',
            name='bucket_all_photo_name',
            field=models.CharField(default='duetin-chorus', max_length=200, verbose_name='\u622a\u56fe\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='allsongmusic',
            name='bucket_all_vedio_name',
            field=models.CharField(default='duetin-chorus', max_length=200, verbose_name='\u5408\u6210\u89c6\u9891\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='allsongmusic',
            name='music_auth_part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auth_music_part', to='dao.PartSongMusic', verbose_name='\u53d1\u5e03\u6b4c\u66f2\u8005\u90e8\u5206\u53f3\u8fb9'),
        ),
        migrations.AlterField(
            model_name='allsongmusic',
            name='music_participant_part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participant_music_part', to='dao.PartSongMusic', verbose_name='\u53c2\u4e0e\u8005\u6b4c\u66f2\u90e8\u5206\u5de6\u8fb9'),
        ),
        migrations.AlterField(
            model_name='musicprofiel',
            name='bucket_accompany_name',
            field=models.CharField(default='duetin-accompany', max_length=200, verbose_name='\u4f34\u594f\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='musicprofiel',
            name='bucket_lyrics_name',
            field=models.CharField(default='duetin-lyrics', max_length=200, verbose_name='\u6b4c\u8bcd\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='partsongmusic',
            name='bucket_caivedio_name',
            field=models.CharField(default='duetin-cuted', max_length=200, verbose_name='\u88c1\u526a\u89c6\u9891\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='partsongmusic',
            name='bucket_part_photo_name',
            field=models.CharField(default='duetin-part', max_length=200, verbose_name='\u622a\u56fe\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='partsongmusic',
            name='bucket_part_vedio_name',
            field=models.CharField(default='duetin-part', max_length=200, verbose_name='\u5408\u6210\u89c6\u9891\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
    ]