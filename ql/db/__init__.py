
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (ForeignKey, Column, Integer, String, DateTime, Float)

Base = declarative_base()

class Exchange(Base):
	"""
	id
	abbrev: short name
	name
	city
	country
	type: stock/foreign exchange/so on...
	describe
	created_date
	last_updated_date
	"""
	__tablename__ = "exchange"

	id = Column(Integer, primary_key=True)
	abbrev = Column(String)
	name = Column(String)
	city = Column(String(255))
	country = Column(String(255))
	type = Column(String(32))
	describe = Column(String(255))
	created_date = Column(DateTime)
	last_updated_date = Column(DateTime)

	def __repr__(self):
		return "<Exchange(id='%s', abbrev='%s', name='%s')>" %(
			self.id, self.abbrev, self.name)


class DailyPrice(Base):
	"""
	"""
	__tablename__ = "daily_price"

	id = Column(Integer, primary_key=True)
	exchange_id = Column(Integer, ForeignKey('exchange.id'))
	open_price = Column(Float)
	high_price = Column(Float)
	low_price = Column(Float)
	close_price = Column(Float)
	volumn = Column(Integer)
	price_date = Column(DateTime)
	created_date = Column(DateTime)
	last_updated_date = Column(DateTime)

	def __repr__(self):
		return "<DailyPrice(id='%s', price_data='%s' open_price='%s', high_price='%s', low_price='%s', close_price='%s', volumn='%s')" %(
			self.id, self.price_date, self.open_price, self.high_price, self.low_price, self.close_price, self.volumn)

