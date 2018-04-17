#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: json_response.py.py
@time: 2017/4/26 下午5:26
@SOFTWARE:PyCharm
"""

from django.http import JsonResponse

from django.utils import six
from rest_framework.response import Response
from rest_framework.serializers import Serializer


def json_resp(data={}, code=0, msg='', context=[]):
    """返回Json"""
    return JsonResponse(dict(result=data, code=code, msg=msg))
    #return JsonResponse({'data': data, 'doce': code, 'msg': msg})


class JsonResponse_zj(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, result=None, code=None, msg=None,
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(result, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {"code": code, "msg": msg, "result": result}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


class JsonResponse_ht(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, total=None,page=None,obj_list=None,page_list=None,page_pre=None,obj_singer=None, code=None, msg=None,title=None,
                 status=None,search_word=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        # if isinstance(result, Serializer):
        #     msg = (
        #         'You passed a Serializer instance as data, but '
        #         'probably meant to pass serialized `.data` or '
        #         '`.error`. representation.'
        #     )
        #     raise AssertionError(msg)

        self.data = {"search_word":search_word,"code": code, "msg": msg, "total":total,"page":page,"obj_list":obj_list,"page_list":page_list,"page_pre":page_pre,"obj_singer":obj_singer,"title":title}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


class JsonResponse_share(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self,obj_list=None, code=None, msg=None,
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        # if isinstance(result, Serializer):
        #     msg = (
        #         'You passed a Serializer instance as data, but '
        #         'probably meant to pass serialized `.data` or '
        #         '`.error`. representation.'
        #     )
        #     raise AssertionError(msg)

        self.data = {"code": code, "msg": msg, "result":obj_list}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value