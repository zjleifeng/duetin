# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-31 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0006_auto_20171023_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(default=b'https://s3-ap-southeast-1.amazonaws.com/duetin-user-tx/default-tx.jpg', max_length=2000, verbose_name='\u5934\u50cf\u5730\u5740'),
        ),
    ]