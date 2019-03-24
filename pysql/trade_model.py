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
    startdate = Column(Date)
    initfund = Column(Float,default=100000)
    trade_fee = Column(Float,default=0.0026)
    accountrade = relationship("Accountrade", back_populates='accountbase',cascade="all, delete, delete-orphan")
    def __repr__(self):
       return "<Accountbase(uuid='%s',type='%s', username='%s', password='%s', email='%s', startdate='%s',initfund='%s',trade_fee='%s')>" % (
                self.uuid,self.type, self.username, self.password,self.email,self.startdate,self.initfund,self.trade_fee)

class Accountrade(Base):
    __tablename__ = 'accountrade'
    id = Column(Integer, primary_key=True)
    accid = Column(Integer, ForeignKey('accountbase.uuid'))
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
    order = relationship("Order", back_populates='accountrade',cascade="all, delete, delete-orphan")
    def __repr__(self):
       return "<Accountrade(accid='%s', max_position='%s', max_hold='%s', realfund='%s', position='%s', primary_strategy='%s', secondary_strategy='%s', recordtime='%s')>" % (
                self.accid, self.max_position, self.max_hold,self.realfund,self.position,self.primary_strategy,self.secondary_strategy,self.recordtime)
    

class Ordertype(Base):
    __tablename__ = 'ordertype'
    id = Column(Integer, primary_key=True)
    type = Column(String,unique=True)
    reorder = Column(Boolean,default=False) #下单失败是否重新下单
    wait = Column(Float,default=0) #重新下单等待时间，秒
    wave = Column(Float,default=0.002) #下单价格允许的波动，默认0.2%
    order = relationship("Order", back_populates='ordertype')
    def __repr__(self):
       return "<Ordertype(type='%s', reorder='%s', wait='%s',wave='%s')>" % (
                self.type, self.reorder, self.wait,self.wave)
    
class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    accid = Column(Integer, ForeignKey('accountrade.accid'))
    type = Column(Integer, ForeignKey('ordertype.id'))
    direction = Column(String,nullable=True)  #B -buy, S -sell
    code = Column(String,nullable=True)
    name = Column(String)
    price = Column(Float)
    share = Column(Integer,nullable=True,default=100)
    status = Column(String,default='ordering') #下单状态
    fee = Column(Float) #交易费用
    ordertime = Column(DateTime,onupdate=func.now)
    ordertype = relationship("Ordertype", back_populates='order')
    accountrade = relationship("Accountrade", back_populates='order')
    def __repr__(self):
       return "<Order(accid='%s', type='%s', direction='%s',code='%s',name='%s',price='%s',share='%s',status='%s',fee='%s',ordertime='%s')>" % (
                self.accid, self.type, self.direction,self.code,self.name,self.price,self.share,self.status,self.ordertime)

class Potential(Base):
    __tablename__ = 'potential'
    id = Column(Integer, primary_key=True)
    code = Column(String,nullable=True)
    name = Column(String)
    weight = Column(Integer,default=1)
    is_valid = Column(Boolean,default=True)
    max_num = Column(Integer,default=100)
    addtime = Column(DateTime)
    lasttime = Column(DateTime,onupdate=func.now)
    def __repr__(self):
       return "<Potential(code='%s', name='%s', weight='%s', is_valid='%s', max_num='%s',addtime='%s')>" % (
                self.code, self.name, self.weight, self.is_valid,self.max_num,self.addtime)

def initial_db(db='pytrader.db',recreate=False):
    if recreate:
        import os
        try:
            backup_db_name = db.replace('.','_bak.')
            if os.path.exists(backup_db_name):
                os.remove(backup_db_name)
            os.renames(db, backup_db_name)
        except Exception as e:
            print('recreate ERROR',e)
    engine = create_engine('sqlite:///' + db + '?check_same_thread=False', echo=False)
    #engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
    #根据基类创建数据库表
    Base.metadata.create_all(engine)
    return

class DBSession:
    def __init__(self,db='pytrader.db',echo=False):
        self.engine = create_engine('sqlite:///' + db + '?check_same_thread=False', echo=echo)
        # 创建DBSession类型:
        Session = sessionmaker(bind=self.engine)
        # DBSession对象可视为当前数据库连接
        # 创建session对象:
        self.session = Session()
    
    def commit(self):
        self.session.commit()
        return
    
    def close(self):
        self.session.close()
        return

    def add_strategy(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        startdate = dt.datetime.now()
        strategy_list = []
        for data in datas:
            """
            if not data[2]:
                print(111)
                sg = Strategy(name=data[0], startdate=data[1] , is_valid=data[3],comments=data[4])
                strategy_list.append(sg)
            else:
                pass
            """
            sg = Strategy(name=data[0], startdate=data[1], lastupdate=data[2] , is_valid=data[3],comments=data[4])
            strategy_list.append(sg)
        #sg = Strategy(name='sell_buy_33', startdate=startdate, is_valid=True,comments='三天低点卖出，三天高点买入')
        #self.session.add(sg)
        #strategy_list = [sg,sg1,sg2,sg3]
        try:
            self.session.add_all(strategy_list)
        except Exception as e:
            print('add_strategy ERROR: ', e)
            return 0
        self.session.commit()
        return 1
    
    def delete_strategy(self,strategy_name):
        try:
            del_sg = dbs.session.query(Strategy).filter_by(name=strategy_name).first()
            dbs.session.delete(del_sg)   
            dbs.session.commit()
        except Exception as e:
            print('delete_strategy ERROR: ', e)
            return 0
        return 1
    
    def set_strategy_valid_status(self,strategy_name,valid=False):
        this_datetime = dt.datetime.now()
        try:
            self.session.query(Strategy).filter(Strategy.name==strategy_name).update({Strategy.is_valid:valid})
            self.session.query(Strategy).filter(Strategy.name==strategy_name).update({Strategy.lastupdate:this_datetime})
            self.session.commit()
        except Exception as e:
            print('set_strategy_valid_status ERROR: ', e)
            return 0
        return 1
    
    def add_account(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        startdate = dt.datetime.now()
        account_list = []
        for data in datas:
            print(data)
            ac = Accountbase(name=data[0], startdate=data[1], lastupdate=data[2] , is_valid=data[3],comments=data[4])
            account_list.append(sg)
        try:
            self.session.add_all(account_list)
        except Exception as e:
            print('add_account ERROR: ', e)
            return 0
        self.session.commit()
        return 1
    
    def delete_account(self,uuid):
        try:
            del_sg = dbs.session.query(Accountbase).filter_by(uuid=uuid).first()
            dbs.session.delete(del_sg)   
            dbs.session.commit()
        except Exception as e:
            print('delete_account ERROR: ', e)
            return 0
        return 1
    
    def update_account(self,uuid,fund):
        this_datetime = dt.datetime.now()
        try:
            self.session.query(Accountbase).filter(Accountbase.uuid==uuid).update({Accountbase.initfund:fund})
            #self.session.query(Accountbase).filter(Accountbase.name==uuid).update({Accountbase.initfund:this_datetime})
            self.session.commit()
        except Exception as e:
            print('update_account ERROR: ', e)
            return 0
        return 1

initial_db(recreate=True)
dbs = DBSession(echo=True)
startdate = dt.datetime.now()
strategy_datas = [('sell_buy_33',startdate,None,True,'三天低点卖出，三天高点买入'),
                  ('fix_exit_3',startdate,None,True,'跌破固定百分比退出'),
                  ('fix_drop_exit',startdate,None,True,'账户最大回撤退出'),
                  ('high_star_exit',startdate,None,True,'高位长上影十字星卖出'),
                  ('ma10_exit',startdate,None,True,'ma10买入和卖出'),
                  ('min_capital',startdate,None,True,'最小市值买入')
                  ]
dbs.add_strategy(strategy_datas)
dbs.set_strategy_valid_status(strategy_name='fix_exit_3',valid=False)
#dbs.delete_strategy(strategy_name='high_star_exit')

    

