# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-03-20 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0013_insbinding'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='recommend_rank',
            field=models.IntegerField(default=0, verbose_name='\u65b0\u7528\u6237\u63a8\u8350\u6392\u5e8f'),
        ),
    ]
