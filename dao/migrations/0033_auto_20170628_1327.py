# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-28 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0032_musicprofiel_is_loved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singer',
            name='uid',
            field=models.CharField(max_length=255, unique=True, verbose_name='\u4e0a\u4f20\u6570\u636e\u552f\u4e00\u6807\u8bc6'),
        ),
    ]
