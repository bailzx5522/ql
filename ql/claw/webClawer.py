import datetime
import urllib2

from ql.claw.base import BaseClaw
from ql.common.log import LOG
from ql.db import DailyPrice, Symbol


class WebClawer(BaseClaw):
    """
    Claw quote from google finance.
    """
    def daily_price_url(self, symbol, start, end):
        """
        get daily from yahoo
        """

        url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % \
            (symbol, start[1] - 1, start[2], start[0], end[1] - 1, end[2], end[0])
        return url

    def get_ticks_url(self, symbol):
        """
        get ticks from google
        """
        interval = 60   #unit(second)
        period = 15     #d(day), Y(year)
        url = "http://www.google.com/finance/getprices?i=%s&p=%s&f=d,o,h,l,c,v&df=cpct&q=%s" % \
            (interval, period, symbol)

        return url

    def data2obj(self, data):
        price = []
        now = datetime.datetime.now()
        for field in data:
            p = field.strip().split(',')
            o = DailyPrice(datetime.datetime.strptime(p[0], '%Y-%m-%d'),
                    p[1], p[2], p[3], p[4], p[5])
            price.append(o)
        return price

def main():
    c = WebClawer()
    url = c.daily_price_url("002222.sz",start=(2013,12,25), end=(2014,12,25))
    #url = c.get_ticks_url("002222")
    print url
    resp = c.send_request(url)
    print resp

if __name__ == '__main__':
    main()