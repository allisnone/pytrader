# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-02-16
#https://docs.python.org/3/library/sqlite3.html
#https://www.sqlite.org/index.html
#https://www.jianshu.com/p/25fde93c2fb9

#https://www.jianshu.com/p/0d234e14b5d3
#https://www.jianshu.com/p/8d085e2f2657
#https://www.jianshu.com/p/9771b0a3e589
#data type
#https://gitee.com/rambo_online/codes/he6xsd9rgyj4ut1l2vw7n73
from sqlalchemy import *#Column, String, create_engine,relationship
from sqlalchemy.orm import sessionmaker,relationship,aliased
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt
from comm.logger import LOG
#from appflask import db
#Base = db.Model
#Column = db.Column
#Integer = db.Integer

# 创建对象的基类:
Base = declarative_base()

class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True)
    startdate = Column(DateTime)
    lastupdate = Column(DateTime)#,onupdate=func.now)
    is_valid = Column(Boolean,default=True)
    comments = Column(Text)
    accountrade = relationship("Accountrade", back_populates='strategy')
    def __repr__(self):
        return "<Strategy(name='%s', startdate='%s', lastupdate='%s', is_valid='%s', comments='%s')>" % (
                            self.name, self.startdate,self.lastupdate, self.is_valid,self.comments)
       
class Accountbase(Base):
    __tablename__ = 'accountbase'
    id = Column(Integer, primary_key=True)
    uuid = Column(String,nullable=True,unique=True)
    type = Column(String,default='A')
    username = Column(String)
    password = Column(String,nullable=True)
    email = Column(String,default='104450966@qq.com')
    startdate = Column(Date,default=dt.datetime.now())
    initfund = Column(Float,default=100000)
    trade_fee = Column(Float,default=0.0026)
    accountrade = relationship("Accountrade", back_populates='accountbase',cascade="all, delete, delete-orphan")
    def __repr__(self):
        return "<Accountbase(uuid='%s',type='%s', username='%s', password='%s', email='%s', startdate='%s',initfund='%s',trade_fee='%s')>" % (
                self.uuid,self.type, self.username, self.password,self.email,self.startdate,self.initfund,self.trade_fee)

class Accountrade(Base):
    __tablename__ = 'accountrade'
    id = Column(Integer, primary_key=True)
    accid = Column(Integer, ForeignKey('accountbase.uuid'),unique=True)
    max_position = Column(Float,default=0.5)
    max_hold = Column(Integer,default=10)
    realfund = Column(Float)
    position = Column(Float)
    primary_strategy = Column(Integer, ForeignKey('strategy.id'),default=1)
    secondary_strategy = Column(Integer)#, ForeignKey('strategy.id'))
    recordtime = Column(DateTime)
    strategy = relationship("Strategy", back_populates='accountrade',foreign_keys=primary_strategy)#,secondary_strategy])
    #strategy = relationship("Strategy", back_populates='accountrade',foreign_keys=secondary_strategy)
    accountbase = relationship("Accountbase", back_populates='accountrade')#,cascade="all, delete, delete-orphan")
    orders = relationship("Orders", back_populates='accountrade')
    is_valid = Column(Boolean,default=True)
    def __repr__(self):
        return "<Accountrade(accid='%s', max_position='%s', max_hold='%s', realfund='%s', position='%s', primary_strategy='%s', secondary_strategy='%s', recordtime='%s',is_valid='%s')>" % (
                self.accid, self.max_position, self.max_hold,self.realfund,self.position,self.primary_strategy,self.secondary_strategy,self.recordtime,self.is_valid)
    

class Ordertype(Base):
    __tablename__ = 'ordertype'
    id = Column(Integer, primary_key=True)
    type = Column(String,unique=True)
    reorder = Column(Boolean,default=False) #下单失败是否重新下单
    wait = Column(Float,default=0) #重新下单等待时间，秒
    wave = Column(Float,default=0.002) #下单价格允许的波动，默认0.2%
    orders = relationship("Orders", back_populates='ordertype')
    def __repr__(self):
        return "<Ordertype(type='%s', reorder='%s', wait='%s',wave='%s')>" % (
                self.type, self.reorder, self.wait,self.wave)
    
class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    accid = Column(Integer, ForeignKey('accountrade.accid'))
    type = Column(Integer, ForeignKey('ordertype.id'))
    direction = Column(String,nullable=True)  #B -buy, S -sell
    code = Column(String,nullable=True)
    name = Column(String)
    price = Column(Float)
    share = Column(Integer,nullable=True,default=100)
    #下单状态: ordering-下单中，ordered-下单成交， partial-下单部分成交，canceled-已取消的下单
    status = Column(String,default='ordering') #下单状态
    fee = Column(Float) #交易费用
    ordertime = Column(DateTime)
    ordertype = relationship("Ordertype", back_populates='orders')
    accountrade = relationship("Accountrade", back_populates='orders')
    deal = relationship("Deal", back_populates='orders')
    def __repr__(self):
        return "<Orders(accid='%s', type='%s', direction='%s',code='%s',name='%s',price='%s',share='%s',status='%s',fee='%s',ordertime='%s')>" % (
                self.accid, self.type, self.direction,self.code,self.name,self.price,self.share,self.status,self.ordertime)

class Deal(Base):
    __tablename__ = 'deal'
    id = Column(Integer, primary_key=True)
    orderid = Column(Integer, ForeignKey('orders.id'))
    price = Column(Float)
    share = Column(Integer,nullable=True,default=100)
    tradetime = Column(DateTime)
    orders = relationship("Orders", back_populates='deal')
    def __repr__(self):
        return "<Deal(orderid='%s', price='%s', share='%s',tradetime='%s')>" % (
                                                                                self.orderid, self.price, self.share,self.tradetime)

class Capital(Base):
    __tablename__ = 'capital'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    #accid = Column(Integer, ForeignKey('accountbase.uuid'),unique=True)
    cash = Column(Float)
    values = Column(Float)
    interval = Column(String,default='D')
    def __repr__(self):
        return "<Capital(time='%s', cash='%s', values='%s','interval='%s')>" % (
                self.time, self.cash, self.values,self.interval)
    
    def get_max_drop(self):
        max_drop = -0.12
        return  max_drop
    
    def dynamic_position(self, max_drop, max_position=1, drop_unit=-0.05):
        #本金连续下跌时应快速减仓
        #max_drop = self.get_max_drop()
        pos = max_position
        n = max_drop/drop_unit
        #n = round(max_drop/drop_unit)
        print('n=',n)
        if n<=1:
            pass
        elif n <3:
            pos = (1+ n * drop_unit*2) * max_position
        else:
            pos = (1+ n * drop_unit * 2) **2 * max_position
        if pos <0.15:
            pos = 0
        return round(min(pos,max_position),2)
    
    def test_position(self):
        max_drop=-0.02
        for i in range(40):
            pos = self.dynamic_position(max_drop)
            print( 'max_drop= {0}, pos={1}'.format(max_drop, pos))
            max_drop = max_drop - 0.01
        
    
class Potential(Base):
    __tablename__ = 'potential'
    id = Column(Integer, primary_key=True)
    code = Column(String,nullable=True)
    name = Column(String)
    weight = Column(Integer,default=1)
    is_valid = Column(Boolean,default=True)
    max_num = Column(Integer,default=100)
    addtime = Column(DateTime)
    lasttime = Column(DateTime)#,onupdate=func.now)
    def __repr__(self):
        return "<Potential(code='%s', name='%s', weight='%s', is_valid='%s', max_num='%s',addtime='%s')>" % (
                self.code, self.name, self.weight, self.is_valid,self.max_num,self.addtime)
