# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-10 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0061_auto_20170930_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicprofiel',
            name='new_sort',
            field=models.IntegerField(default=0, verbose_name='NEW\u9875\u9762\u624b\u52a8\u6392\u5e8f'),
        ),
        migrations.AlterField(
            model_name='postdata',
            name='mp4_key_name',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='\u89c6\u9891KEY'),
        ),
    ]
