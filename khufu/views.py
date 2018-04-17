#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/4/26 下午12:10
@SOFTWARE:PyCharm
"""

# coding=utf8
import datetime
from django.utils.timezone import utc
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from khafre.utils.json_response import json_resp, JsonResponse_zj

from django.shortcuts import render
from six.moves.urllib_parse import quote

from social_core.utils import sanitize_redirect, user_is_authenticated, \
                   user_is_active, partial_pipeline_data, setting_url

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 1)


def index(request):
    return render(request, 'include/index/index.html')

def policy(request):
    return render(request,'include/index/policy.html')

class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if EXPIRE_HOURS>0:
                utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)

                if created or token.created < utc_now - datetime.timedelta(hours=EXPIRE_HOURS):
                    token.delete()
                    token = Token.objects.create(user=serializer.validated_data['user'])
                    token.created = utc_now
                    token.save()

                return Response({'token': token.key})
            else:
                return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

def complete(request, *args, **kwargs):
    user=request.user
    token=Token.objects.get(user_id=user).key
    return json_resp(code=200,msg='ok',data={"token":token})




def page_not_found(request):
    return render(request, 'include/error/404.html')


def page_error(request):
    return render(request, 'include/error/500.html')


def permission_denied(request):
    return render(request, 'include/error/403.html')