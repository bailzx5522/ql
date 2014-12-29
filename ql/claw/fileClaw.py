
import os
import datetime

from ql.claw.base import BaseClaw
from ql.db import Symbol as db_symbol
from ql.db import sql_api as db

class fileClaw(BaseClaw):

    def __init__(self, path):
        self.fpath = path

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
        symbols = []
        now = datetime.datetime.now()
        for d in data:
            symbol = db_symbol(d['Short_name'], None, d['Code'], "sz_stock", None, now)
            symbols.append(symbol)
        return symbols
       
    def restore(self, symbols):
        db.insert_symbols(symbols)


if __name__ == "__main__":
    file = fileClaw("/opt/ql/data/shenzhen_exchange_list")
    dict = file.read()
    symbols = file.data2obj(dict)
    file.restore(symbols)
