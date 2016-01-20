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
        stocks = pd.DataFrame()
    logging.info("Fetch from db %s stocks" % len(stocks.index))
    if len(stocks.index) < 2000:
        stocks = stocks_clawer()
    return stocks

def all_tick_clawer(save=True):
    df = ts.get_today_all()
    if save is True:
        _save_db(df, db_ticks_table)
    return df

def stock_tick_clawer(code, save=True):
    df = ts.get_realtime_quotes(code)
    if save is True:
        _save_db(df, db_ticks_temp_table)
    return df

def history_clawer(code, s=None, e=None, ktype=None, save=True):
    logging.info("Fetch stock:%s %s-%s %s histroy data" % (code,s,e,ktype))
    #sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板
    index = ["sh", "sz", "hs", "sz50", "zxb", "cyb"]

    df = ts.get_hist_data(code, start=s, end=e, ktype=ktype)
    print type(df)
    df["code"] = df["open"].map(lambda x:code)
    print df.columns
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
