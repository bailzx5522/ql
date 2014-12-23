

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ql.db import Exchange, DailyPrice


engine = create_engine("mysql://root@localhost:3306/data_repo")
Session = sessionmaker(bind=engine)

def get_session():
	if Session is None:
		Session = sessionmaker(bind=engine)
	s = Session()
	return s

def insert_exchange(**kwargs):
	pass


def get_exchange(name=None, id=None):
	session = get_session()
	return session.query(Exchange).\
			filter_by(name=name).\
			filter_by(id=id).all()

def insert_prices(prices):
	session = get_session()
	# assert prices is a list of objects of DailyPrice
	print len(prices)
	session.add_all(prices)
	session.commit()

def get_price(id=None):
	session = get_session()
	return session.query(DailyPrice).\
				filter_by(exchange_id=id).all()
