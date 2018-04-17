# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-18 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0021_auto_20170516_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='partsongmusic',
            name='vedio_url',
            field=models.CharField(default=1, max_length=200, verbose_name='\u4e0e\u4f34\u594f\u5408\u6210\u540e\u89c6\u9891MP4\u5730\u5740'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='musicprofiel',
            name='Original_file',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u539f\u5531\u97f3\u9891\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='partsongmusic',
            name='view_count_rank',
            field=models.IntegerField(default=0, verbose_name='\u70ed\u95e8\u6392\u5e8f'),
        ),
        migrations.AlterField(
            model_name='partsongmusic',
            name='voice_url',
            field=models.CharField(max_length=200, verbose_name='\u4e0e\u4f34\u594f\u5408\u6210\u540e\u97f3\u9891AAC\u5730\u5740'),
        ),
    ]