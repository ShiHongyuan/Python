#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shihongyuan'

'''
定义API的错误对象
'''

import json, logging, inspect, functools


class Page(object):
    '''
    翻页组件
    '''
    def __init__(self, item_count, page_index, page_size=10):
        # 总条数
        self.item_count = item_count
        # 请求哪一页
        self.page_index = page_index
        # 默认每页10条
        self.page_size = page_size
        # 计算总页数
        self.page_count = item_count // page_size + (1 if item_count % page_size else 0)
        if item_count == 0 or page_index > self.page_count:
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            # 根据请求页数求数据库读取开始位置和条数，用于limit
            self.offset = self.page_size * (self.page_index - 1)
            self.limit = self.page_size * self.page_index
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__


class APIError(Exception):
    '''
    包含错误类型，错误数据，错误信息的基本错误对象
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message


class APIValueError(APIError):
    '''
    input输入错误或无效的错误对象
    field 是错误的input字段
    '''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value: invalid', field, message)


class APIResourceNotFoundError(APIError):
    '''
    资源未找到，resource是资源名
    '''
    def __init__(self, resource, message):
        super(APIResourceNotFoundError, self).__init__('resource: notfound', resource, message)


class APIPermissionError(APIError):
    '''
    无权限
    '''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission: forbidden', 'permission', message)

