
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (ForeignKey, Column, Integer, String, DateTime, Float)

Base = declarative_base()

class Symbol(Base):
    """
    create table symbol (
        id integer AUTO_INCREMENT,
        abbrev varchar(36),
        name varchar(36),
        type varchar(36),
        description varchar(255),
        created_at date,
        PRIMARY KEY (id));
    """
    __tablename__ = "symbol"

    id = Column(Integer, primary_key=True)
    abbrev = Column(String)
    name = Column(String)
    type = Column(String(32), default="stock")
    description = Column(String(255))
    created_at = Column(DateTime)

    def __init__(self, abbrev, name, type, description, ctime):
        self.abbrev = abbrev
        self.name = name
        self.type = type
        self.description = description
        self.created_at = ctime
    def __repr__(self):
        return "<Exchange(id='%s', abbrev='%s', name='%s')>" %(
            self.id, self.abbrev, self.name)


#class Fundamental(Base):
#    """
#    Fundamental a symbol related.
#    create table fundamental (
#        symbol_id integer,
#        TODO
#        FOREIGN KEY (symbol_id) REFERENCE symbol(id));
#    );
#    """
#    __tablename__ = "fundamental"
#
#    symbol_id = Column(Integer)
#    
#    def __init__(self, symbol_id):
#        self.symbol_id = symbol_id
#
#    def __repr__(self):
#        return "<Fundamental(symbol_id=%s)>" % (self.symbol_id)


class DailyPrice(Base):
    """
    create table daily_price (
        id integer AUTO_INCREMENT,
        symbol_id integer,
        open decimal(5,2),
        high decimal(5,2),
        low decimal(5,2),
        close decimal(5,2),
        volume integer,
        price_date date,
        created_at datetime,
        primary key (id),
        FOREIGN KEY (symbol_id) REFERENCES symbol(id));
    """
    __tablename__ = "daily_price"

    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey('symbol.id'))
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    price_date = Column(DateTime)
    created_at = Column(DateTime)

    def __init__(self, price_date, open, high, low, close, volume, ctime):
        self.price_date = price_date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.created_at = ctime

    def __repr__(self):
        return "<DailyPrice(id='%s', price_data='%s' open='%s', high='%s', low='%s', close='%s', volume='%s')" %(
            self.id, self.price_date, self.open, self.high, self.low, self.close, self.volume)

class Tick(Base):
    __tablename__ = 'tick'

    id = Column(Integer, primary_key = True)
    symbol = Column(String(12))
    time = Column(Integer)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

    def __init__(self, symbol, time, open, high, low, close, volume):
        ''' constructor '''
        self.symbol = symbol
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __repr__(self):
        return "<Tick('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
           % (self.symbol, self.time, self.open, self.high, self.low, self.close, self.volume)
