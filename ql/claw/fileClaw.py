
import os
import datetime

from ql.claw.base import BaseClaw
from ql.db import Symbol as db_symbol
from ql.db import Tick as db_tick
from ql.db import sql_api as db

class fileClaw(BaseClaw):

    def __init__(self, path, split="\t"):
        self.fpath = path
        self.symbol_info = self._parse_name()
        self.split = split

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

        ret = []
        fd = open(self.fpath, "r")
        lines = fd.readlines()[2:-1]
        for line in lines:
        #column(20120101 0935 open high low close volumn amount)
            field = line.strip().split(self.split)
            piece = {"date":field[0], "time":field[1], "open":field[2],
                        "high":field[3], "low":field[4], "close":field[5],
                        "volume":field[6], "amount":field[7]}
            ret.append(piece)
        return ret

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
        db.insert_symbols(symbols)

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
    db.insert_symbols(data)

def insert_price():
    files = parse_files('/opt/ql/data/stock_data')
    for file in files:
        claw = fileClaw(file)
        data = claw.read_tdx()
        symbol = db.get_symbol_by_code(claw.symbol_info.code)
        ticks = []
        for p in data:
            time_str = p['date'] +" "+ p['time']
            obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H%M")
            tick = db_tick(symbol.id, None, obj, p['open'], p['high'],
                            p['low'], p['close'], p['volume'])
            ticks.append(tick)
        db.insert_ticks(ticks)
        print "file:%s is ok" % file

if __name__ == "__main__":
    #create_symbol()
    
    insert_price()
