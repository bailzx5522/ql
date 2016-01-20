
import pandas as pd

from abc import ABCMeta, abstractmethod

from ql.db.sql_api import get_engine

class Strategy(object):
    def __init__(self):
        pass

    def generate_signal(self):
        pass

    def get_data_from_db(self, symbol_id, interval):
        sql = "select * from tick where symbol_id=%s order by price_date desc limit %s"
        db_con = get_engine()
        df = pd.read_sql_query(sql%(symbol_id, interval), db_con)
        self.data = df
        return self.data

    def sma(self, period=10, apply='close'):
        self.data['sma'] = pd.rolling_mean(self.data[apply], period, 1)
        return self.data

    def macd(self, p1):
        pass
