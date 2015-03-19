
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (ForeignKey, Column, Integer, String, DateTime, Float)

Base = declarative_base()

class Symbol(Base):
    """
    create table symbol (
        id integer AUTO_INCREMENT,
        abbrev varchar(32),
        name varchar(32),
        code varchar(32),
        type varchar(32),
        created_at datetime,
        PRIMARY KEY (id));
    """
    __tablename__ = "symbol"

    id = Column(Integer, primary_key=True)
    abbrev = Column(String(32))
    name = Column(String(32))
    code = Column(String(32))
    volume = Column(String(32))
    type = Column(String(32), default="stock")
    created_at = Column(DateTime)

    def __init__(self, abbrev, name, code, volume, type, description, ctime):
        self.abbrev = abbrev
        self.name = name
        self.code = code
        self.volume = volume
        self.type = type
        self.created_at = ctime

    def __repr__(self):
        return "<Exchange(id='%s', abbrev='%s', code='%s')>" %(
            self.id, self.abbrev, self.code)


class classify(Base):

    __tablename__ = "classify"
    
    id = Column(Integer, primary_key=True)
    type = Column(String(36))
    describe = Column(String(255))
    index = Column(Integer)

    def __init__(self, type, index=0, describe=None):
        self.type = type
        self.describe = describe
        self.index = index


class SymbolClassify(Base):
    __tablename__ = "symbol_classify_relation"

    classify_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, primary_key=True)

    def __init__(self, c_id, s_id):
        self.classify_id = c_id
        self.symbol_id = s_id


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

    def __init__(self, symbol_id, price_date, open, high, low, close, volume, ctime):
        self.symbol_id = symbol_id
        self.price_date = price_date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.created_at = ctime

    def __repr__(self):
        return "<DailyPrice(id='%s', symbol(id)='%s', price_data='%s' open='%s',\
                 high='%s', low='%s', close='%s', volume='%s')" % \
                (self.id, self.symbol_id, self.price_date, self.open, self.high,
                    self.low, self.close, self.volume)

class Tick(Base):
    __tablename__ = 'tick'

    id = Column(Integer, primary_key = True)
    symbol_id = Column(Integer, ForeignKey('symbol.id'))
    price_date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    amount = Column(Float)

    def __init__(self, symbol, price_date, open, high, low, close, volume, amount):
        ''' constructor '''
        self.symbol_id = symbol
        self.price_date = price_date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.amount = amount

    def __repr__(self):
        return "<Tick('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
           % (self.symbol_id, self.price_date, self.open,
                self.high, self.low, self.close, self.volume, self.amount)
