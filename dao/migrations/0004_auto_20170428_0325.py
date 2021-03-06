# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-28 03:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dao', '0003_auto_20170428_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='allsongmusic',
            name='all_music_auth',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='my_all_post', to=settings.AUTH_USER_MODEL, verbose_name='\u53d1\u5e03\u4eba'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partsongmusic',
            name='music_auth',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_part_post', to=settings.AUTH_USER_MODEL, verbose_name='\u53d1\u5e03\u4eba'),
        ),
    ]
