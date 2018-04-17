#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: edition.py
@time: 2017/12/26 下午1:10
@SOFTWARE:PyCharm
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from rest_framework.templatetags.rest_framework import replace_query_param
from rest_framework.versioning import BaseVersioning
from rest_framework.exceptions import APIException

class VERSIONERO(APIException):
    status_code = 430
    default_detail = _('Not found.')
    default_code = 'not_found'


class Version_check(BaseVersioning):
    """
    GET /something/?version=0.1 HTTP/1.1
    Host: example.com
    Accept: application/json
    """
    invalid_version_message = _('Invalid version in query parameter.')

    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get(self.version_param, self.default_version)
        if not self.is_allowed_version(version):
            raise VERSIONERO("version error!")
        return version

    def reverse(self, viewname, args=None, kwargs=None, request=None, format=None, **extra):
        url = super(QueryParameterVersioning, self).reverse(
            viewname, args, kwargs, request, format, **extra
        )
        if request.version is not None:
            return replace_query_param(url, self.version_param, request.version)
        return url
