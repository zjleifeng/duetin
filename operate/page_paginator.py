#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: page_paginator.py
@time: 2017/10/16 下午2:15
@SOFTWARE:PyCharm
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/28 17:06
# @Author  : eric
# @Site    :
# @File    : page_paginator.py
# @Software: PyCharm

from django.core.paginator import Paginator
from math import ceil


class DuetinPaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=3, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num
        self._max_pages=self._count = None


    def page(self, number):
        self.page_num = number
        return super(DuetinPaginator, self).page(number)


    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
            return range(1, self.num_pages + 1)
        num_list = []
        num_list.append(int(self.page_num))
        for i in range(1, int(self.range_num) + 1):
            if int(self.page_num) - i <= 0:
                num_list.append(num_count + int(self.page_num) - i)
            else:
                num_list.append(int(self.page_num) - i)

            if int(self.page_num) + i <= int(self.num_pages):
                num_list.append(int(self.page_num) + i)
            else:
                num_list.append(int(self.page_num) + i - num_count)
        num_list.sort()
        return num_list


    def _get_max_pages(self):

        if self._max_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._max_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._max_pages = int(ceil(hits / float(self.per_page)))-4
        return self._max_pages

    max_pages=property(_get_max_pages)
    page_range_ext = property(_page_range_ext)