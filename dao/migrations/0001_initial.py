# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-27 10:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ALLComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': '\u5408\u5531\u6b4c\u66f2\u8bc4\u8bba\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='AllSongMusic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u6807\u9898')),
                ('photo', models.CharField(max_length=200, verbose_name='\u663e\u793a\u56fe\u7247')),
                ('vedio', models.CharField(max_length=200, verbose_name='\u89c6\u9891')),
                ('voice_url', models.CharField(max_length=200, verbose_name='\u97f3\u9891\u5730\u5740')),
                ('praise', models.BigIntegerField(default=0, verbose_name='\u88ab\u8d5e\u6b21\u6570')),
                ('view_count', models.BigIntegerField(default=0, verbose_name='\u89c2\u770b\u6b21\u6570')),
                ('share_count', models.BigIntegerField(default=0, verbose_name='\u5206\u4eab\u6b21\u6570')),
                ('rank', models.IntegerField(default=0, verbose_name='\u624b\u52a8\u6392\u5e8f')),
                ('view_count_rank', models.FloatField(default=0, verbose_name='\u70ed\u95e8\u6392\u5e8f')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u4ee5\u52a0\u5165')),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': '\u5408\u5531\u6b4c\u66f2\u6570\u636e\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='\u6807\u9898')),
                ('content', models.TextField(blank=True, null=True, verbose_name='\u4ecb\u7ecd\u8bf4\u660e')),
                ('img', models.CharField(default=b'banner/default.jpg', max_length=300, verbose_name='\u56fe\u7247\u5730\u5740')),
                ('link', models.CharField(blank=True, max_length=300, null=True, verbose_name='\u8d85\u94fe\u63a5')),
                ('rank', models.IntegerField(default=0, verbose_name='\u624b\u52a8\u6392\u5e8f')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u6392\u5e8f')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'BANNER\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='MusicProfiel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_name', models.CharField(max_length=200, verbose_name='\u6b4c\u66f2\u540d')),
                ('language', models.IntegerField(blank=True, choices=[(0, 'CHN'), (1, 'ENG')], null=True, verbose_name='\u8bed\u8a00')),
                ('Original_file', models.CharField(max_length=200, verbose_name='\u539f\u5531\u97f3\u9891\u6587\u4ef6')),
                ('accompany', models.CharField(max_length=200, verbose_name='\u4f34\u594f\u6587\u4ef6')),
                ('k_game', models.CharField(max_length=200, verbose_name='\u6253\u5206\u6587\u4ef6')),
                ('lyrics', models.CharField(max_length=200, verbose_name='\u6b4c\u8bcd\u6587\u4ef6')),
                ('image', models.CharField(max_length=200, verbose_name='\u6b4c\u66f2\u5c01\u9762\u56fe\u7247')),
                ('view_times', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6b21\u6570')),
                ('rank', models.IntegerField(default=0, verbose_name='\u624b\u52a8\u6392\u5e8f')),
                ('is_delete', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e0a\u67b6')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '\u6b4c\u66f2\u4fe1\u606f\u5173\u7cfb',
            },
        ),
        migrations.CreateModel(
            name='PartComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': '\u534a\u9996\u6b4c\u8bc4\u8bba\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='PartSongMusic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u6807\u9898')),
                ('auth_photo', models.CharField(max_length=200, verbose_name='\u5531\u6b4c\u4eba\u663e\u793a\u56fe\u7247')),
                ('auth_vedio', models.CharField(max_length=200, verbose_name='\u5531\u6b4c\u8005\u89c6\u9891')),
                ('voice_url', models.CharField(max_length=200, verbose_name='\u97f3\u9891\u5730\u5740')),
                ('socre', models.IntegerField(default=100, verbose_name='\u5f97\u5206')),
                ('match_count', models.BigIntegerField(default=0, verbose_name='\u88ab\u5408\u5531\u6b21\u6570')),
                ('praise', models.BigIntegerField(default=0, verbose_name='\u88ab\u8d5e\u6b21\u6570')),
                ('view_count', models.BigIntegerField(default=0, verbose_name='\u89c2\u770b\u6b21\u6570')),
                ('rank', models.IntegerField(default=0, verbose_name='\u624b\u52a8\u6392\u5e8f')),
                ('view_count_rank', models.FloatField(default=0, verbose_name='\u70ed\u95e8\u6392\u5e8f')),
                ('share_count', models.BigIntegerField(default=0, verbose_name='\u5206\u4eab\u6b21\u6570')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u4ee5\u52a0\u5165')),
                ('is_delete', models.BooleanField(default=False)),
                ('music_auth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_music_auth', to=settings.AUTH_USER_MODEL, verbose_name='\u5531\u6b4c\u8005')),
                ('music_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='music', to='dao.MusicProfiel', verbose_name='\u6b4c\u66f2\u6570\u636e')),
            ],
            options={
                'verbose_name_plural': '\u534a\u9996\u6b4c\u6570\u636e\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singer_name', models.CharField(max_length=200, verbose_name='\u6b4c\u624b')),
                ('singer_country', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u6240\u5c5e\u56fd\u5bb6')),
                ('sex', models.IntegerField(blank=True, choices=[(0, 'MAN'), (1, 'women')], null=True, verbose_name='\u6027\u522b')),
                ('rank', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('photo', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u6b4c\u624b\u56fe\u7247')),
                ('singer_ico', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u6b4c\u624b\u5934\u50cf')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name_plural': '\u6b4c\u624b\u7ba1\u7406',
            },
        ),
        migrations.AddField(
            model_name='partcomment',
            name='music',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='part_music_comment', to='dao.PartSongMusic', verbose_name='\u6240\u5c5e\u89c6\u9891'),
        ),
        migrations.AddField(
            model_name='partcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dao.PartComment', verbose_name='\u7236\u7ea7\u8bc4\u8bba'),
        ),
        migrations.AddField(
            model_name='partcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partcomment_user', to=settings.AUTH_USER_MODEL, verbose_name='\u8bc4\u8bba\u4eba'),
        ),
        migrations.AddField(
            model_name='musicprofiel',
            name='snger_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='singer', to='dao.Singer'),
        ),
        migrations.AddField(
            model_name='allsongmusic',
            name='music_auth_part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auth_music_part', to='dao.PartSongMusic', verbose_name='\u53d1\u8d77\u8005\u6b4c\u66f2\u90e8\u5206'),
        ),
        migrations.AddField(
            model_name='allsongmusic',
            name='music_participant_part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participant_music_part', to='dao.PartSongMusic', verbose_name='\u53c2\u4e0e\u8005\u6b4c\u66f2\u90e8\u5206'),
        ),
        migrations.AddField(
            model_name='allcomment',
            name='music',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='all_music_comment', to='dao.AllSongMusic', verbose_name='\u6240\u5c5e\u89c6\u9891'),
        ),
        migrations.AddField(
            model_name='allcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dao.ALLComment', verbose_name='\u7236\u7ea7\u8bc4\u8bba'),
        ),
        migrations.AddField(
            model_name='allcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL, verbose_name='\u8bc4\u8bba\u4eba'),
        ),
    ]
