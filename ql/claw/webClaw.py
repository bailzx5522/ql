import datetime
import urllib2

from ql.common.log import LOG
from ql.claw import claw
from ql.db import DailyPrice, Exchange


class WebClaw(claw.Claw):

	def claw(self):

		url = self.generate_url()

		data, status_code = self.send_request(url)

		if status_code == 200:
			prices = self.data2obj(data)
		else:
			print status_code
			return None

		
		self.restore(prices)

	def generate_url(self):

		if self.provider == 'yahoo':
			url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % \
				(self.symbol, self.start[1] - 1, self.start[2], self.start[0], self.end[1] - 1, self.end[2], self.end[0])
			return url
		elif self.provider == 'google':
			return None
		else:
			return None

	def data2obj(self, data):
		price = []
		now = datetime.datetime.now()
		for field in data:
			o = DailyPrice()
			p = field.strip().split(',')
			o.price_date = datetime.datetime.strptime(p[0], '%Y-%m-%d')
			o.open_price = p[1]
			o.high_price = p[2]
			o.low_price = p[3]
			o.close_price = p[4]
			o.volumn = p[5]
			o.created_date = now
			o.last_updated_date = now
			price.append(o)
		return price

def main():
	c = WebClaw("003311.sz",start=(2014,12,1), end=(2014,12,3))
	c.claw()

if __name__ == '__main__':
	main()
