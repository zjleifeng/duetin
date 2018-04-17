# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-18 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0073_auto_20171117_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='allsongmusic',
            name='all_gif_bucket',
            field=models.CharField(default='duetin-all-gif', max_length=200, verbose_name='all\u90e8\u5206gif\u56fe\u7247bucket'),
        ),
        migrations.AddField(
            model_name='allsongmusic',
            name='all_gif_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='all\u90e8\u5206gif\u56fe\u7247key'),
        ),
        migrations.AddField(
            model_name='allsongmusic',
            name='all_gif_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='GIF\u56fe\u7247\u5730\u5740'),
        ),
        migrations.AddField(
            model_name='musicprofiel',
            name='segments',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u8f6c\u573ajson\u6587\u4ef6'),
        ),
        migrations.AddField(
            model_name='musicprofiel',
            name='segments_bucket_name',
            field=models.CharField(default='duetin-segments', max_length=200, verbose_name='\u8f6c\u573a\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='musicprofiel',
            name='segments_key_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u8f6c\u573a\u6587\u4ef6bucket\u7684key'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='one_gif_bucket',
            field=models.CharField(default='duetin-one-gif', max_length=200, verbose_name='part\u90e8\u5206gif\u56fe\u7247bucket'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='one_gif_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='part\u90e8\u5206gif\u56fe\u7247key'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='one_jpg_bucket',
            field=models.CharField(default='duetin-one-jpg', max_length=200, verbose_name='part\u90e8\u5206jpg\u56fe\u7247bucket'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='one_jpg_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='part\u90e8\u5206jpg\u56fe\u7247key'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='part_gif_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='GIF\u56fe\u7247\u5730\u5740'),
        ),
    ]