# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-28 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0075_auto_20171226_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='allsongmusic',
            name='share_jpg_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='share\u56fe\u7247key'),
        ),
    ]
