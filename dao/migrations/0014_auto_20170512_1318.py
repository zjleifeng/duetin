# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-12 05:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0013_auto_20170512_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musicprofiel',
            name='singer_name',
        ),
        migrations.AddField(
            model_name='musicprofiel',
            name='singer',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='singer_info', to='dao.Singer'),
            preserve_default=False,
        ),
    ]
