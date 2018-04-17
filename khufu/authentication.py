#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: authentication.py
@time: 2017/4/26 下午12:19
@SOFTWARE:PyCharm
"""
# coding=utf8
import datetime
from django.utils.timezone import utc
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from khafre.utils.json_response import json_resp

from django.core.cache import caches
cache_token = caches['token']

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 1)


class ExpiringTokenAuthentication(TokenAuthentication):
    """Set up token expired time"""

    def authenticate_credentials(self, key):
        # Search token in cache
        cache_user = cache_token.get(key)
        if cache_user:
            return (cache_user, key)

        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)

        if EXPIRE_HOURS>0:
            if token.created < utc_now - datetime.timedelta(hours=EXPIRE_HOURS):
                token.delete()
                return json_resp(code=400,msg='Token has expired then delete.')
                # raise exceptions.AuthenticationFailed(_('Token has expired then delete.'))

            if token:
                # Cache token
                cache_token.set(key, token.user, EXPIRE_HOURS*60*60)

        else:
            if token:

                cache_token.set(key, token.user, timeout=0)

        return (token.user, token)
        #


from django.contrib.auth import logout
def social_user(backend, uid, user=None, *args, **kwargs):
    '''OVERRIDED: It will logout the current user
    instead of raise an exception '''

    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
            # msg = 'This {0} account is already in use.'.format(provider)
            # raise AuthAlreadyAssociated(backend, msg)

        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}