#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : test_package.py
@Author: crawlSpider
@Address: https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%BD%91%E8%99%ABspider&ie=utf8&_sug_=n&_sug_type_=
@Github: https://github.com/qi20172017
@Date  : 2021/7/24 上午9:15
@Desc  : 
"""

from example_package import example


if __name__ == '__main__':
    res = example.add_one(3)
    print(res)