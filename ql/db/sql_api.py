"""
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ql.db import Symbol, DailyPrice


_MAKER = None
_ENGINE = None

def get_engine():
    return create_engine("mysql://root@localhost:3306/ql")

def get_maker(engine):
    return sessionmaker(bind=engine)

def get_session():
    global _MAKER, _ENGINE
    if _ENGINE is None:
        _ENGINE = get_engine()
        session = get_maker(_ENGINE)
    else:
        session = get_maker(_ENGINE)
    return session()

def insert_symbols(symbols):
    session = get_session()
    session.add_all(symbols)
    session.commit()


def get_symbol_by_code(code):
    session = get_session()
    return session.query(Symbol).\
            filter_by(code=code).first()

def get_symbols():
    session = get_session()
    return session.query(Symbol).all()


def insert_prices(prices):
    session = get_session()
    session.add_all(prices)
    session.commit()

def get_price(id=None):
    session = get_session()
    return session.query(DailyPrice).\
                filter_by(exchange_id=id).all()

###########################TICK######################
def insert_ticks(ticks):
    session = get_session()
    session.add_all(ticks)
    session.commit()
