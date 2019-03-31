# -*- coding:utf-8 -*-
import datetime,time
from sqlalchemy import *#Column, String, create_engine,relationship
from sqlalchemy.orm import sessionmaker,relationship,aliased
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

# 创建对象的基类:
Base = declarative_base()
def get_hist_data(code,strategy='33'):
    pos = 1.0
    next_buy = 1
    next_sell = 1
    next_sell_high = 0
    if strategy=='33':
        pass
    else:
        is_last_hight_start = True
        great_increase= True
        if is_last_hight_start and great_increase:
            #向上挂卖,成功卖出后：若新高，重新买入，否则，第二天观察：若第二天再触发卖出，清仓.
            next_sell_high = 0.33 * next_sell + 0.67 * next_buy
            #大于next_buy ,重新买入
            pos = 0.5
            delay = 60*60
        else:
            pass
    return next_buy,next_sell,pos,next_sell_high

class strategy33(object):
    def __init__(self,code):
        next_buy,next_sell,pos = get_hist_data(code)
        self.buy = next_buy
        self.sell = next_sell
        self.pos = pos

class hist(Base):
    __tablename__ = 'hist'
    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer)
    code = Column(String,unique=True)
    laststatus = Column(Integer) #卖1，买-1，保持不变0
    lastprice = Column(Float)
    lastdate = Column(DateTime)
    pos = Column(Float,default=1.0)
    next_price = Column(Float)
    thisdata = Column(DateTime)
    cash = Column(Float,default=0.0)
    share = Column(Float)
    
    def set_last_trade(self,status,price,lastdate):
        self.laststatus = status
        self.lastprice = price
        self.lastdate = lastdate
    
    def set_pos(self,pos):
        self.pos = pos
    
    def get_next_price(self):
        price = 0
        stg33 = strategy33(self.code)
        if self.laststatus==-1: #上一次买入
            price = stg33.sell
        elif self.laststatus==1: #上一次卖出,
            price = -1 * stg33.buy
        else:
            pass
        return price