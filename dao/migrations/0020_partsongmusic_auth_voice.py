# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-15 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0019_auto_20170515_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='partsongmusic',
            name='auth_voice',
            field=models.CharField(default=1, max_length=200, verbose_name='\u5531\u6b4c\u8005\u539f\u59cb\u97f3\u9891'),
            preserve_default=False,
        ),
    ]
