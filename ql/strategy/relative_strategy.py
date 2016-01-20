import pandas as pd
import numpy as np
import math

from ql.lib import time_utils
from ql.lib.plot import Plot
from ql.strategy import Strategy


class SRStrategy(Strategy):
	"""
	This strategy compare relative strongth of some stocks.
	"""
	def __init__(self):
		pass

	def get_data(self, symbols, interval):
		data_set = pd.DataFrame()
		for sym in symbols:
			data = self.get_symbol_from_db(sym)
			if data:
				data_set[sym] = s_data['close']
				ind = Index(s_data['price_date'])
				data_set.set_index(ind)
			else:
				raise "ERROR"

	def compare(self):
		pass

def main():
	s = SRStrategy()
	symbols = ['2150', '2151']
	s.get_data(symbols, "288")



if __name__ == "__name__":
	main()
