#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: operatelog.py
@time: 2017/11/10 上午11:42
@SOFTWARE:PyCharm
"""
from dao.models.base import OperationLogs


def operationlogs(request, object_old_model, dict_update_fields, msg):
    """
    操作日志
    :param object_old_model: 旧的model对象实例
    :param dict_update_fields: 更新的字段键值对--字典格式
    :param type: 类型 (自己定义)
    :param msg: 自定义日志内容 (如果日志格式非‘A由aa变为bb’，可使用此参数)
    :return:
    """
    content = ''

    if object_old_model is not None and dict_update_fields is not None:

        fielddic = getmodelfield(object_old_model)

        obj_id = object_old_model.id
        obj_rep = object_old_model._meta.db_table

        for key, val in dict_update_fields.items():

            _rtn = compare(getattr(object_old_model, key), val, fielddic[key])

            content = _rtn
            if content == "":
                pass
            else:
                OperationLogs.objects.create(object_id=obj_id, object_rep=obj_rep, type=msg, change_message=content,
                                             user=request.user)

    else:
        content = ""


def getmodelfield(modelname):
    """获取model 指定字段的 verbose_name属性值"""
    fielddic = {}
    for field in modelname._meta.fields:
        fielddic[field.name] = field.name
    return (fielddic)


def compare(oldstr, newstr, field):
    """
    生成操作日志详细记录
    :param oldstr: 原值
    :param newstr: 新值
    :param field: 目标字段
    :return: content
    """
    content = ''
    type_o = type(oldstr)
    type_n = type(newstr)

    if type_n == type_o:
        old_str = oldstr
        new_str = newstr
    else:
        if type_o == bool:
            new_str = bool(newstr)
            old_str = oldstr
        else:
            new_str = type_n(newstr)
            old_str = type_n(oldstr)

    if oldstr == None:
        oldstr = ""

    if old_str == new_str:  # 值未变化，不做处理
        pass
    else:
        if oldstr == "":
            oldstr = "None"

        content = ('"%s"由"%s"变为"%s";' % (field, oldstr, newstr))

    return content