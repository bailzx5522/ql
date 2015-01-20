
import pandas as pd
import numpy as np
import math

from ql.strategy import Strategy
from ql.db.sql_api import get_engine


class MMStrategy(Strategy):
    """
    Max and min price in day, consist a support/resistent area.
    So sell at the resistent, and buy at the support lines.
    """
    def __init__(self, data):
        self.data = data

    def _select(self, l):
        ordered = l.order()
        print ordered.values

    def get_rs(self):
        df = self.data.copy()
        grouped = df.groupby('date')
        day_high = grouped['high'].max()
        day_low = grouped['low'].min()
        #day_high.apply(self._select, args=(day_high,))

        #support = self._select(day_low)
        resistance = self._select(day_high)

    def generate_signal(self):
        pass


def main():
    sql = "select * from tick where symbol_id = 8 order by price_date desc limit 1440"
    db_con = get_engine()
    df = pd.read_sql_query(sql, db_con)
    s = MMStrategy(df)
    s.get_rs()


if __name__ == '__main__':
    main()
