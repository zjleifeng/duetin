# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-19 05:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0059_postdata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allsongmusic',
            options={'ordering': ['-view_count', '-created_at'], 'verbose_name_plural': '\u5408\u5531\u6b4c\u66f2\u6570\u636e\u7ba1\u7406'},
        ),
    ]
