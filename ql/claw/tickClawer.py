import datetime
import time
import urllib2
from threading import Thread

from ql.claw.base import BaseClaw
from ql.common.log import LOG
from ql.db import Tick, Symbol
from ql.db import sql_api as db_api


class tickClawer(BaseClaw):
    """
    Claw quote from google finance.
    """
    def __init__(self, symbols, start=None, end=None):
        self.symbols = symbols
        self.start = start
        self.end = end
        self.tick_interval = 60     #unit(second). Google finance support 60s at least.
        self.tick_period = "15d"    #d(day), Y(year)

    def read(self, url, proxy=None):
        try:
            if proxy:
                import socks
                import socket
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7000)
                socket.socket = socks.socksocket
                import urllib2
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            return resp
        except urllib2.URLError, e:
            print e
            return None
        except Exception as e:
            print e
            return None

    def get_ticks_url(self, symbol):
        """
        get ticks from google
        """
        # .SZ MUST BE upper
        code = symbol.code+".SZ" if symbol.type=="sz_stock" else symbol.code
        url = "http://www.google.com/finance/getprices?i=%s&p=%s&f=d,o,h,l,c,v&df=cpct&q=%s" % \
            (self.tick_interval, self.tick_period, code)
        return url

    def data2obj(self, id, data):
        price = []
        day_open = None
        for field in data:
            p = field.strip().split(',')
            # db:id date o h l c v
            # data:DATE,CLOSE,HIGH,LOW,OPEN,VOLUME
            if 'a' in p[0]:
                day_open = int(p[0][1:])
                o = Tick(id, day_open, p[4], p[2], p[3], p[1], p[5])
            else:
                if day_open is None:
                    print "ERROR====================================symbol_id:%s, field:%s"%(id, field)
                    return None
                o = Tick(id, day_open+60*int(p[0]), p[4], p[2], p[3], p[1], p[5])
            price.append(o)
        return price

    def restore(self, prices):
        try:
            db_api.insert_prices(prices)
        except:
            print prices[0]

    def _worker(self, symbol):
        url = self.get_ticks_url(symbol)
        print url
        LOG.debug(url)
        resp = self.read(url, proxy=True)
        if resp is None:
            LOG.error(resp)
            return
        data = resp.readlines()
        prices = self.data2obj(symbol.id, data[8:])
        if prices:
            self.restore(prices)

    def fetch_save_symbols(self, pools=10):
        counter = 0
        while counter < len(self.symbols):
            size = len(self.symbols) - counter
            if size > pools:
                size = pools
            process_symbols = self.symbols[counter: counter+size]

            threads = []
            for s in process_symbols:
                thread = Thread(name=s, target=self._worker, args=[s])
                thread.daemon = True
                thread.start()

                threads.append(thread)

            for thread in threads:
                thread.join(120)

            counter += size

            # sleep for 3 second to avoid being blocked by google...
            time.sleep(5)
        
def main():
    symbols = db_api.get_symbols()
    #symbols = db_api.get_symbol_by_code("002020")
    c = tickClawer(symbols)
    c.fetch_save_symbols()

    #symbols = db_api.get_symbol_by_code("002222")
    #c = tickClawer(symbols)
    #url = c.get_ticks_url(symbols[0])
    #lines = c.read(url, proxy=True).readlines()
    #prices = c.data2obj(symbols[0].id, lines[8:])
    #c.restore(prices)
   
if __name__ == '__main__':
    main()
