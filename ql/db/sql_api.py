"""
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ql.db import Symbol, DailyPrice


_MAKER = None

def get_engine():
    return create_engine("mysql://root@localhost:3306/ql")

def get_maker(engine):
    return sessionmaker(bind=engine)

def get_session():
    global _MAKER
    if _MAKER is None:
        engine = get_engine()
        session = get_maker(engine)
    return session()

def inster_symbols(symbols):
    session = get_session()
    session.add_all(symbols)


def get_exchange(name=None, id=None):
    session = get_session()
    return session.query(Symbol).\
            filter_by(name=name).\
            filter_by(id=id).all()

def insert_prices(prices):
    session = get_session()
    session.add_all(prices)
    session.commit()

def get_price(id=None):
    session = get_session()
    return session.query(DailyPrice).\
                filter_by(exchange_id=id).all()
