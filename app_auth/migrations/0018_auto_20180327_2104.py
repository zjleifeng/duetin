# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-03-27 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0017_mobileversion_error_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture_key_name',
            field=models.CharField(blank=True, default=b'default-tx.jpg', max_length=200, null=True, verbose_name='\u5934\u50cf\u6587\u4ef6bucket\u7684key'),
        ),
    ]
