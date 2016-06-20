#--coding:utf-8--
#=================TODO LIST===================
#1. DATA
##1.1 TD DATA
##1.2 数据格式
##1.2.1 数据格式
##1.3 没了，那个软件唯一数据来源就是龙虎榜。。。
#2. DATA Analysis
##2.1 按照institute
###2.1.1 跟踪每个inst介入后的走势
##2.2 按照broker
##2.3 按照stock
##2.4 按照操作类型

import tushare as ts

from ql.lib import time_utils

def get_td_list(date=None):
    """
    description: 每日榜单
    params:
        date: 日期
    """
    if date is None:
        date = time_utils.today()
    data = ts.top_list(date)
    return data

def get_td_cap_list(days=5, retry=3, pause=0):
    """
    description:n日内上榜的累积卖出和买入
    params:
        days: n
        retry: 重试次数
        pause: 重启间隔
    """
    data = ts.cap_tops(days=days, retry_count=retry, pause=pause)
    return data

def get_td_broker_list(days=5, retry=3, pause=0):
    """
    获取营业部买入卖出情况
    """
    data = ts.broker_tops(days=days, retry_count=retry, pause=pause)
    return data

def get_td_inst_list(days=5, retry=3, pause=0):
    """
    上榜票列表
    """
    data = ts.inst_tops(days=days, retry_count=retry, pause=pause)
    return data

def get_td_inst_detail(retry=3, pause=0):
    """
    最近一天
    """
    data = ts.inst_detail(retry_count=retry, pause=pause)
    return data

def get_td_top_detail(code, date=None, retry=3, pause=0):
    """
    description:当日，榜单交易详情
    params:
    return:
    """
    data = ts.top_detail(code, date=date, retry_count=retry, pause=pause)
    return data

for i in range(1, 2):   # month 1th
    for j in range(1, 7):   # day 1-6th
        try:
            date = "2016-%s-%s" % (i, j)
            data = get_td_list(date=date)
            if data is None:
                print date + " is None"
            else:
                print data["code"]
                for stock_code in data["code"]:
                    print get_td_top_detail(stock_code, date=date)
        except:
            print date + " is passed"
#print get_td_top_detail("000766", date="2016-06-08")
