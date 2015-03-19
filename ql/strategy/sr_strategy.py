
import pandas as pd
import numpy as np
import math

from ql.lib.time_utils
from ql.lib.plot import Plot
from ql.strategy import Strategy


class MMStrategy(Strategy):
    """
    Max and min price in day, consist a support/resistent area.
    So sell at the resistent, and buy at the support lines.
    """
    def __init__(self):
        pass

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
        #print ordered
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
        #print pd.Series(ret, dtype=float)
                
    def generate_signal(self):
        pass


def main():
    s = MMStrategy()
    s.get_data_from_db("2150", "1440")
    s.get_rs()
    print time_utils.pd_tf_convert(s.data)
    #p = Plot(s.sma())
    #p.draw()


if __name__ == '__main__':
    main()
