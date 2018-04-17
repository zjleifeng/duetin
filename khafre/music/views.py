# -*- coding: utf-8 -*-

"""
Create at 2017/3/30
"""

__author__ = 'TT'
from rest_framework import viewsets, permissions
#from serilizers import BannerSerializer
from .permission import IsAdminCreateOnly
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from dao.models.music import PartSongMusic
from khafre.main.serilizers import PartSongMusicSerializer
from dao.models.base import Banner


class SongBookRecommendView(viewsets.ModelViewSet):
    """唱歌页面推荐歌曲VIEW"""
    queryset = PartSongMusic.objects.all().filter(is_enable=True).filter(is_delete=False)
    serializer_class = PartSongMusicSerializer


class SongBookNewView(viewsets.ModelViewSet):
    """唱歌页面最新歌曲view"""
    queryset = PartSongMusic.objects.all().filter(is_enable=True).filter(is_delete=False).order_by('-created_at')
    serializer_class = PartSongMusicSerializer



