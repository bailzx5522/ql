"""
	Base class about claw data from various ways.

"""

import urllib2

from ql.db import api as db


class Claw(object):
	"""
	Base class:
		fetch from everywhere.
	parameters:
		symbol:

		provider:
			data provider.google/yahoo
		start:
			Format:(YYYY,M,D)
		end:
			Format:(YYYY,M,D)
	"""
	def __init__(self, provider='yahoo', symbol=None, start=None, end=None):
		self.provider = provider
		self.symbol = symbol or []
		self.start = self._get_time(start)
		self.end = self._get_time(end)

	def _get_time(self, t):
		if t:
			#TODO
			return t
		else:
			return None

	def send_request(self, url):
		try:
			resp = urllib2.urlopen(url)
			code = resp.getcode()
			data = resp.readlines()[1:]
			return code, data
		except urllib2.HTTPError as e:
			return None, e
		except Exception as e:
			return None, e

	def claw(self):
		pass

	def generate_url(self):
		pass

	def read_files(self, files):
		pass

	def data2obj(self, data, obj):
		pass

	def restore(self, prices):
		db.insert_prices(prices)