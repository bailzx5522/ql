
import pandas as pd
import numpy as np
import math

#from ql.lib.plot import Plot
from ql.strategy import Strategy
from ql.db.sql_api import get_engine


class MMStrategy(Strategy):
    """
    Max and min price in day, consist a support/resistent area.
    So sell at the resistent, and buy at the support lines.
    """
    def __init__(self, data):
        self.data = data

    def get_rs(self):
        df = self.data.copy()
        max = df.max(index=1)['close']
        min = df.min(index=1)['close']
        result = []
        rows = len(df)
        for index, row in df.iterrows():
            close = row['close']
            begin = index-11 if index>11 else 0
            end = index+11 if index<rows-11 else rows-11
            if close == df['close'][begin:end].max():
                result.append(close)
        sp = pd.Series(result, dtype=float)

        last = 0
        ret = []
        ordered = sp.order()
        print ordered
        for i,v in ordered.iteritems():
            if last == 0:
                last = v
                bias = v*0.01
                ret.append(v)
            elif v - last <= bias:
                pass
            elif v - last > bias:
                ret.append(v)
            last = v
            bias = v*0.01
        print pd.Series(ret, dtype=float)
                
    def generate_signal(self):
        pass


def main():
    sql = "select * from tick where symbol_id = 8 order by price_date desc limit 1440"
    db_con = get_engine()
    df = pd.read_sql_query(sql, db_con)
    s = MMStrategy(df)
    s.get_rs()
	#p = Plot(data)
	#p.draw()


if __name__ == '__main__':
    main()
