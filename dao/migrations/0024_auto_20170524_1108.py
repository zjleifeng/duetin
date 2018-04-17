# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-24 03:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0023_auto_20170518_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allmusicpraise',
            name='music',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='allmusic_praise', to='dao.AllSongMusic', verbose_name='\u6240\u5c5e\u6b4c\u66f2'),
        ),
    ]