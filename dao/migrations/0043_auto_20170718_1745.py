# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-18 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0042_auto_20170718_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allcomment',
            name='text',
            field=models.CharField(max_length=250, verbose_name='\u8bc4\u8bba\u5185\u5bb9'),
        ),
    ]