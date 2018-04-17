# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-02-08 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0087_auto_20180206_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongException',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u6b4c\u66f2\u540d')),
                ('singer_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u6b4c\u624b\u540d')),
                ('case_option', models.IntegerField(blank=True, choices=[(1, b'Cannot find song'), (2, b'Wrong research result')], null=True, verbose_name='\u95ee\u9898\u7c7b\u578b')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='\u95ee\u9898\u63cf\u8ff0')),
                ('is_settle', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5904\u7406')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name_plural': '\u641c\u7d22\u6b4c\u66f2\u5f02\u5e38\u7ba1\u7406',
            },
        ),
    ]
