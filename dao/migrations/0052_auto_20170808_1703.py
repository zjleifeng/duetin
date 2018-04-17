# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-08 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dao', '0051_auto_20170807_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partsongmusic',
            old_name='bucket_part_vedio_name',
            new_name='part_vedio_bucket_name',
        ),
        migrations.RenameField(
            model_name='partsongmusic',
            old_name='bucket_part_vedio_key',
            new_name='part_vedio_key',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='auth_photo',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='auth_vedio',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='auth_voice',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='bucket_caivedio_key',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='bucket_caivedio_name',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='bucket_part_photo_key',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='bucket_part_photo_name',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='match_count',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='praise',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='share_count',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='vedio_url',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='view_count',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='view_count_rank',
        ),
        migrations.RemoveField(
            model_name='partsongmusic',
            name='voice_url',
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='aac_bucket_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u4e0a\u4f20\u7684\u539f\u59cb\u97f3\u9891key'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='aac_bucket_name',
            field=models.CharField(default='duetin-android-upaac', max_length=200, verbose_name='\u4e0a\u4f20\u7684\u539f\u59cb\u97f3\u9891bucket'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='cuted_bucket_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u89c6\u9891\u5e72\u58f0\u5408\u6210\u540e\u89c6\u9891key'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='cuted_bucket_name',
            field=models.CharField(default='duetin-cuted', max_length=200, verbose_name='\u89c6\u9891\u5e72\u58f0\u5408\u6210\u540e\u89c6\u9891bucket'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='hc_aac_bucket_name',
            field=models.CharField(default='duetin-hc-voice', max_length=200, verbose_name='\u97f3\u9891\u4f34\u594f\u5408\u6210\u540ebucket'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='hc_aac_key_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u97f3\u9891\u4f34\u594f\u5408\u6210\u540ekey'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='pydub_bucket_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u8c03\u6574\u540e\u97f3\u9891key'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='pydub_bucket_name',
            field=models.CharField(default='duetin-processing', max_length=200, verbose_name='\u8c03\u6574\u540e\u97f3\u9891bucket'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='vedio_bucket_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u4e0a\u4f20\u7684\u539f\u59cb\u89c6\u9891key'),
        ),
        migrations.AddField(
            model_name='partsongmusic',
            name='vedio_bucket_name',
            field=models.CharField(default='duetin-android-upmp4', max_length=200, verbose_name='\u4e0a\u4f20\u7684\u539f\u59cb\u89c6\u9891bucket'),
        ),
    ]
