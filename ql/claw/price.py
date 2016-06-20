# -*- coding: utf-8 -*-

import logging
import os
import sqlite3
import sqlalchemy
import sys
import pandas as pd
import tushare as ts

from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(filename='/tmp/ql_clawer.log', level=logging.DEBUG)

"""
Return of tushare module is pandas object.core.frame.DataFrame object
历史行情数据
复权历史数据
实时行情数据
历史分笔数据
实时报价数据
当日历史分笔
大盘指数列表
大单交易数据
"""
engine = None
db_path = "../data/download.db"
db_stocks_table = "stocks"
db_history_table = "history"
db_ticks_table = "ticks"
db_ticks_temp_table = "ticks_temp"

def stocks_clawer(save=True):
    logging.info("Fetch from remote!")
    df = ts.get_stock_basics()
    logging.info("Fetch %s stocks from remote!"% len(df.index))
    if save is True:
        _save_db(df, db_stocks_table, if_exists="replace", index_label="code")
    return df

def get_stock_list():
    sql = "select * from stocks"
    try:
        stocks = _query_db(sql)
    except Exception as e:
        print e
        stocks = stocks_clawer()
    logging.info("Fetch from db %s stocks" % len(stocks.index))
    return stocks

def all_tick_clawer(save=True):
    df = ts.get_today_all()
    if save is True:
        _save_db(df, db_ticks_table)
    return df

def get_tick_history(code, retry_count=3, pause=0, save=True):
    """
    Description:
        历史分笔交易（每tick成交量，用于发现大单成交）
    Params:
        code
    """
    df = get_tick_data()
    if save is True:
        pass
    return df

def get_tick_today(code, retry_count=3, pause=0, save=True):
    """
    Description:
        当日已经产生的分笔交易详情
    Params:
        code
    """
    df = get_today_ticks(code,retry_count=retry_count, pause=pause)
    if save is True:
        pass
    return df

#实时分笔（当前时间的1-5档挂单情况，用于跟踪实时买卖盘，撤单，交易细节）
def stock_tick_now(code, save=True):
    """
    Description:
    Params:
    code:6位数字股票代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
         可输入的类型：str、list、set或者pandas的Series对象
    """
    df = ts.get_realtime_quotes(code)
    if save is True:
        _save_db(df, db_ticks_temp_table)
    return df

def history_clawer(code, s=None, e=None, ktype=None, save=True):
    logging.info("Fetch stock:%s %s-%s %s period histroy data" % (code,s,e,ktype))
    #sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板
    index = ["sh", "sz", "hs", "sz50", "zxb", "cyb"]

    df = ts.get_hist_data(code, start=s, end=e, ktype=ktype)
    df["code"] = df["open"].map(lambda x:code)
    _save_db(df, db_ticks_table)
    return df

def _get_engine():
    global engine
    if engine is None:
        engine = sqlite3.connect(db_path)
        engine.text_factory = str
    return engine

def _save_db(df, table_name, index=True, index_label=None, if_exists="append"):
    e = _get_engine()
    df.to_sql(table_name, e, if_exists=if_exists, index=index, index_label=None)

def _query_db(sql):
    e = _get_engine()
    df = pd.read_sql(sql, e)
    return df

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "-b":
        # run as a backgroud server
        # 1. save histroy data /everyday(price/tick order)
        # 2. temporary save realtime data for runtime analysis
        # 3.
        sched = BlockingScheduler()
        sched.add_job(my_job, 'interval', seconds=5)
        sched.start()
    else:
        stocks = get_stock_list()
        for code in stocks["code"]:
            history_clawer(code, ktype='5')
