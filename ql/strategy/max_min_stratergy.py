
import pandas as pd

from ql.strategy import Strategy
from ql.db.sql_api import get_engine


class MMStratergy(Strategy):
    """
    Max and min price in day, consist a support/resistent area.
    So sell at the resistent, and buy at the support lines.
    """
    def __init__(self, data):
        self.data = data


    def get_rs(self):
        df = self.data.copy()
        grouped = df.groupby('date')
        day_high = grouped['high'].max()
        day_low = grouped['low'].min()
        print day_high.values

    def generate_signal(self):
        pass


def main():
    sql = "select * from tick where symbol_id = 8 order by price_date desc limit 1440"
    db_con = get_engine()
    df = pd.read_sql_query(sql, db_con)
    s = MMStratergy(df)
    s.get_rs()


if __name__ == '__main__':
    main()
