# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-26 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0074_auto_20171218_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='allsongmusic',
            name='photo_key_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u5408\u6210\u56fe\u7247\u7684key'),
        ),
        migrations.AlterField(
            model_name='musicprofiel',
            name='bucket_image_name',
            field=models.CharField(default='duetin-music-image', max_length=200, verbose_name='\u6b4c\u66f2\u56fe\u7247\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
    ]
