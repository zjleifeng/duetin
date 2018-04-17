# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-01-26 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0084_remove_postdata_reverberation'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdata',
            name='old_part',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u65e7\u7684PART\u90e8\u5206ID'),
        ),
        migrations.AddField(
            model_name='postdata',
            name='old_participant',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u65e7\u7684participant\u90e8\u5206ID'),
        ),
        migrations.AddField(
            model_name='postdata',
            name='part_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='PART\u90e8\u5206ID'),
        ),
    ]
