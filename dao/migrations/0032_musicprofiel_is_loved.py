# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-28 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0031_auto_20170620_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicprofiel',
            name='is_loved',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u7537\u5973\u5408\u5531'),
        ),
    ]