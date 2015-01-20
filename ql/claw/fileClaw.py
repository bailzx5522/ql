
import os
import datetime

import pandas as pd
import numpy as np

from ql.claw.base import BaseClaw
from ql.db import Symbol as db_symbol
from ql.db import Tick as db_tick
from ql.db import sql_api as db_api

class fileClaw(BaseClaw):

    def __init__(self, path, split="\t"):
        self.fpath = path
        self.symbol_info = self._parse_name()
        self.split = split
        self.db_con = db_api.get_engine()

    def _parse_name(self):
        self.file_name = self.fpath.split('/')[-1]
        #sh/sz
        locale = self.file_name[0:2].lower()
        code = int(self.file_name[2:8])
        index = 0
        if code <= 2000:
            #sz
            type = "sz"
        elif code <= 3000:
            #sz & zhongxiao
            type = "zx"
        elif code <=300999:
            #sz & chuangye
            type = "cy"
        elif code >= 600000 and code <= 610000:
            #sh
            type = "sh"
        else:
            type = "index"
            index = 1
        now = datetime.datetime.now()
        return db_symbol(None, None, code, "stock", None, now)
        

    def read_tdx(self):
        if self.fpath is None:
            return None
        col_names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount']
        data = pd.read_csv(self.fpath, sep=self.split, index_col=False,
                            skiprows=2, skip_footer=1, names=col_names)
        # merge date+time = price_date
        data['price_date'] = data.date+" "+data.time.map(lambda i: str(i) if i>999 else "0"+str(i))
        data['price_date'] = data['price_date'].map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H%M'))
        symbol = self._get_symbol(self.symbol_info.code)
        data['symbol_id'] = symbol.id
        return data

    def _unique_field(self, field, df):
        symbol = self._get_symbol(self.symbol_info.code)
        sql = "select %s from tick where symbol_id=%s" %(field, symbol.id)
        o_df = pd.read_sql_query(sql, self.db_con)
        return df[~df['price_date'].isin(o_df['price_date'])]

    def _get_symbol(self, code):
        return db_api.get_symbol_by_code(code)

    def read(self):
        """
        Read file
        Return diction
        """
        if self.fpath is None:
            return None
        fd = open(self.fpath, "r")
        lines = fd.readlines()
        titles = lines[0].split(" ")
        exchanges = []
        print titles
        for line in lines[1:]:
            ar = line.split(' ')
            exchg = {}
            for index,key in enumerate(titles):
                try:
                    exchg[key.strip()] = ar[index].strip()
                except IndexError:
                    print key
                    exchg[key.strip()] = None
            exchanges.append(exchg)
        fd.close()
        return exchanges

    def data2obj(self, data):
        """
        Input:
            data: dict of data.
        Output:
            A list of Symbol object.
        """
        symbols = []
        now = datetime.datetime.now()
        for d in data:
            symbol = db_symbol(d['Short_name'], None, d['Code'], "sz_stock", None, now)
            symbols.append(symbol)
        return symbols
       
    def restore(self, symbols):
        db_api.insert_symbols(symbols)

    def to_sql(self, df):
        df.to_sql("tick", self.db_con, flavor='mysql', if_exists='append', index=False)
        

def parse_files(dir):
    full_path = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            full_path.append(root + '/' + file)
    return full_path

def create_symbol():
    files = parse_files('/opt/ql/data/stock_data')
    data = []
    for file in files:
        claw = fileClaw(file)
        data.append(claw.symbol_info)
    db_api.insert_symbols(data)

def insert_price():
    files = parse_files('/opt/ql/data/stock_data')
    #files = ["/opt/ql/data/stock_data/SZ002312.TXT"]
    for file in files:
        claw = fileClaw(file)
        df = claw.read_tdx()
        new_df = claw._unique_field("price_date", df)
        claw.to_sql(new_df)

if __name__ == "__main__":
    #create_symbol()
    insert_price()
