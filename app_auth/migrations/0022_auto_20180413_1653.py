# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-04-13 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0021_auto_20180410_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='\u751f\u65e5\u65f6\u95f4\u6233'),
        ),
    ]