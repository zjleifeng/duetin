#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: pags.py
@time: 2017/5/10 下午1:42
@SOFTWARE:PyCharm
"""
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status

from .json_response import JsonResponse_zj,JsonResponse_ht,JsonResponse_share
from khufu.settings import PAGE_SIZE,PAGE_NUM
from django.http import JsonResponse

from relationships import Relationship
from django.core.cache import caches
from khufu.settings import redis_ship

import redis

r = Relationship(redis_ship)


def api_paging(singer, song, Serializer_singer, Serializer_song, request, type=None, return_count=None):
    """
    搜索歌手歌曲返回分页数据
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    try:
        if return_count:
            page_size = return_count
        else:
            page_size=PAGE_SIZE
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return JsonResponse_zj(code=414, msg='page and page_size must be integer!')
    if page==1:
        serializer_singer = Serializer_singer(singer, many=True)
    else:
        serializer_singer=None
    if song:
        paginator = Paginator(song, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            song_data = paginator.page(page)
        except PageNotAnInteger:
            song_data = paginator.page(1)
        except EmptyPage:
            # song = paginator.page(paginator.num_pages)
            song_data = None
            page = total
        if song_data:
            serializer_song = Serializer_song(song_data, many=True)
        else:
            serializer_song=None
        # serializer_singer = Serializer_singer(singer, many=True)
    else:
        serializer_song=None
        total=1
    if not serializer_singer and not serializer_song:
        return JsonResponse_zj(code=420, msg='not data')

    elif serializer_singer and not serializer_song:
        return JsonResponse_zj(result={
            'data_singer': serializer_singer.data,
            'data_song': [],
            'page': page,
            'total': total,
            'type': type
        }, code=200, msg='ok')
    elif serializer_song and not serializer_singer:
        return JsonResponse_zj(result={
            'data_singer': [],
            'data_song': serializer_song.data,
            'page': page,
            'total': total,
            'type': type
        }, code=200, msg='ok')
    else:
        return JsonResponse_zj(result={
            'data_singer': serializer_singer.data,
            'data_song': serializer_song.data,
            'page': page,
            'total': total,
            'type': type
        }, code=200, msg='ok')

def nei_paging(objs, serializer_obj, request):
    # 暂时废弃不使用
    """
    个人用户中个人post作品分页显示
    :param objs: 
    :param serializer_obj: 
    :param request: 
    :return: 
    """
    try:
        page_size = int(request.GET.get('page_size', PAGE_SIZE))
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return JsonResponse_zj(code=414, msg='page and page_size must be integer!')
    if objs:
        paginator = Paginator(objs, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            # obj = paginator.page(paginator.num_pages)
            obj = None
            page = total
        serializer = serializer_obj(obj, many=True, context={'request': request})
        data = {
            'my_all_post': serializer.data,
            'page': page,
            'total': total
        }
        return data

    else:
        return {"my_all_post": []}

        # return JsonResponse_zj(result={
        #         'my_all_post': serializer.data,
        #         'page': page,
        #         'total': total
        #     }, code=200, msg='ok')
        #     return None


def js_resp_sing_paging(objs, request, serializer_obj, serializer_banner):
    # 暂时废弃
    """
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    try:
        page_size = int(request.GET.get('page_size', PAGE_SIZE))
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return JsonResponse_zj(code=414, msg='page and page_size must be integer!')
    if objs:
        paginator = Paginator(objs, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            # obj = paginator.page(paginator.num_pages)
            obj = None
            page = total
        serializers = serializer_obj(obj, many=True)

    else:
        return JsonResponse_zj(code=420, msg='not data')

    return JsonResponse_zj(result={
        'data_banner': serializer_banner,
        'data': serializers.data,
        'page': page,
        'total': total
    }, code=200, msg='ok')

def js_resp_htpg(objs, request, serializer_obj, obj_singer=None, pages=None,pagenum=None,title=None,search_word=None):
    """
    OK

    code：
    414:page and page_size must be integer!
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    if pagenum:
        page_num=pagenum
    else:
        page_num=PAGE_NUM
    if pages:
        page_size = pages
        page = int(request.GET.get('page', 1))
    else:
        try:
            page_size = int(request.GET.get('page_size', page_num))
            page = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            return JsonResponse_zj(code=414, msg='page and page_size must be integer!')
    if objs:
        paginator = Paginator(objs, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            # obj = paginator.page(paginator.num_pages)
            obj = None
            page = total
        if page > 1:
            page_pre = page - 1
        else:
            page_pre = 0

        num_count = 2 * 3 + 1
        if total <= num_count:
            num_list= range(1, total + 1)
        else:
            num_list = []
            num_list.append(int(page))
            for i in range(1, 3 + 1):
                if int(page) - i <= 0:
                    num_list.append(num_count + int(page) - i)
                else:
                    num_list.append(int(page) - i)

                if int(page) + i <= int(total):
                    num_list.append(int(page) + i)
                else:
                    num_list.append(int(page) + i - num_count)
        num_list.sort()
        # if total>1 and total in num_list:
        #     num_list.remove(total)
        page_list = num_list

        # page_list = range(2, total + 1)
        serializers = serializer_obj(obj, many=True, context={'request': request})

    else:
        return JsonResponse_ht(search_word=search_word,title=title,obj_singer=obj_singer,code=420, msg='not data')

    if serializers.data:

        return JsonResponse_ht(search_word=search_word,title=title,total=total, page=page, obj_list=serializers.data, page_list=page_list,
                               page_pre=page_pre, obj_singer=obj_singer, code=200,
                               msg='ok')

    else:
        return JsonResponse_ht(search_word=search_word,title=title,obj_singer=obj_singer,code=420, msg='not data')



def js_resp_paging(objs, request, serializer_obj, pages=None):
    """
    OK

    code：
    414:page and page_size must be integer!
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    if pages:
        page_size = pages
        page = int(request.GET.get('page', 1))
    else:
        try:
            page_size = int(request.GET.get('page_size', PAGE_SIZE))
            page = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            return JsonResponse_zj(code=414, msg='page and page_size must be integer!')
    if objs:
        paginator = Paginator(objs, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            # obj = paginator.page(paginator.num_pages)
            obj = None
            page = total
        serializers = serializer_obj(obj, many=True, context={'request': request})

    else:
        return JsonResponse_zj(code=420, msg='not data')

    if serializers.data:

        return JsonResponse_zj(result={
            'data': serializers.data,
            'page': page,
            'total': total
        }, code=200, msg='ok')
    else:
        return JsonResponse_zj(code=420, msg='not data')

    
def js_resp_newuser_paging(objs, request, serializer_obj,is_following, pages=None):
    """
    新用户，feed页面推荐专用
    OK

    code：
    414:page and page_size must be integer!
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    if pages:
        page_size = pages
        page = int(request.GET.get('page', 1))
    else:
        try:
            page_size = int(request.GET.get('page_size', PAGE_SIZE))
            page = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            return JsonResponse_zj(code=414, msg='page and page_size must be integer!')
    if objs:
        paginator = Paginator(objs, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            # obj = paginator.page(paginator.num_pages)
            obj = None
            page = total
        serializers = serializer_obj(obj, many=True, context={'request': request})

    else:
        return JsonResponse_zj(code=420, msg='not data')

    if serializers.data:

        return JsonResponse_zj(result={
            'data': serializers.data,
            'page': page,
            'total': total,
            "is_following":is_following
        }, code=200, msg='ok')
    else:
        return JsonResponse_zj(code=420, msg='not data')

def js_is_friend_resp(objs, request, serializer_obj):
    """
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    try:
        page_size = int(request.GET.get('page_size', PAGE_SIZE))
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return JsonResponse_zj(code=414, msg='page and page_size must be integer!')
    if objs:
        paginator = Paginator(objs, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            # obj = paginator.page(paginator.num_pages)
            obj = None
            page = total
        serializers = serializer_obj(obj, many=True)
        import json
        li = list(serializers.data)

        for i in li:
            user_id = i['id']
            my_id = request.user.id
            if r(my_id).is_following(user_id):
                i['is_following'] = True
            else:
                i['is_following'] = False

        js_str = json.dumps(li)

        js_ok = json.loads(js_str)



    else:
        return JsonResponse_zj(code=400, msg='not data')
    if js_ok:
        return JsonResponse_zj(result={
            'data': js_ok,
            'page': page,
            'total': total
        }, code=200, msg='ok')
    else:
        return JsonResponse_zj(code=420, msg='not data')



def js_resp_share(objs, request, serializer_obj):
    """
    OK

    code：
    414:page and page_size must be integer!
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """

    if objs:
        serializers = serializer_obj(objs, context={'request': request})

    else:
        return JsonResponse_share(code=420, msg='not data')

    if serializers.data:

        return JsonResponse_share(obj_list=serializers.data, code=200,msg='ok')

    else:
        return JsonResponse_share(code=420, msg='not data')
