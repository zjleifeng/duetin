# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-17 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0056_auto_20170817_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partsongmusic',
            name='part_vedio_bucket_name',
            field=models.CharField(default='duetin-part', max_length=200, verbose_name='\u5408\u6210\u89c6\u9891\u6587\u4ef6BUCKET\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='partsongmusic',
            name='part_vedio_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u5408\u6210\u89c6\u9891\u6587\u4ef6bucket\u7684key'),
        ),
    ]