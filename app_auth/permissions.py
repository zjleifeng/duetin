#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: permissions.py
@time: 2017/5/5 下午2:42
@SOFTWARE:PyCharm
"""
from rest_framework import permissions
from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect


perm_dic = {
    'view_operate_list':['userlogin','GET',[]],# 权限字段名称(models表中定义)，URL别名,GET方法,请求参数
    # 'view_operate_list': ['userlogin', 'GET', []],  # 权限字段名称(models表中定义)，URL别名,GET方法,请求参数

    # 'view_customer_info':['customer_detail','GET',[]],
    # 'edit_own_customer_info':['customer_detail','POST',['qq','name']],  # GET为查询，POST提交数据
}


def perm_check(*args, **kwargs):
    request = args[0]
    # 反向解析request中url
    url_resovle_obj = resolve(request.path_info)
    current_url_namespace = url_resovle_obj.url_name
    print "url namespace:", current_url_namespace
    matched_flag = False
    matched_perm_key = None
    # 如果正确反解析出了url且其在权限字典中
    if current_url_namespace is not None:
        print "find perm item ..."
        for perm_key in perm_dic:
            perm_val = perm_dic[perm_key]
            if len(perm_val) == 3:
                url_namespace, request_method, request_args = perm_val
                # 如果request中的url、get方法与权限列表中相同
                if url_namespace == current_url_namespace:
                    if request.method == request_method:
                        # 如果权限列表中无请求参数，此时已可以确定找到了权限规则
                        if not request_args:
                            matched_flag = True
                            matched_perm_key = perm_key
                            print 'matched perm ...'
                            break
                        else:
                            # 如果权限列表中有请求的参数，反射出request中get或post数据
                            request_method_func = getattr(request, request_method)
                            # 如果权限列表中所有请求参数都与反射出的参数匹配，则证明权限匹配成功
                            for request_arg in request_args:
                                if request_method_func.get(request_arg) is not None:
                                    matched_flag = True
                                else:
                                    # 一旦有不匹配的情况，则证明权限已经匹配错误，后续无须再做判断
                                    matched_flag = False
                                    print "request arg[%s] not matched" % request_arg
                                    break
                            # 如果此条规则匹配成功，不需要再做后续其它规则的匹配
                            if matched_flag == True:
                                print "--passed permission check --"
                                matched_perm_key = perm_key
                                break
    else:
        # 如果request解析出的url与urls不匹配，放过？？？
        return True
    # request请求与权限规则已匹配
    if matched_flag == True:
        perm_str = 'crm.%s' % matched_perm_key
        # 如果用户被授与此权限，返回True，否则返回False
        if request.user.has_perm(perm_str):
            print "\033[42;1m ------ permission checked -------\033[0m"
            return True
        else:
            print "\033[41;1m ------- no permission --------\033[0m"
            print request.user, perm_str
            return False
    else:
        print "\033[41;1m ------ no matched permission ----- \033[0m"


def check_permission(func):
    def wrapper(*args, **kwargs):
        print "--start check perms", args[0]
        if not perm_check(*args, **kwargs):
            return render(args[0], 'include/index.html')
        return func(*args, **kwargs)

    return wrapper


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
