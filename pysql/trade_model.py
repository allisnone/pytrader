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
from logs.mylogger import LOG

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
            LOG.logger.error('initial_db: {}'.format(e))
            #print('recreate ERROR',e)
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
        try:
            self.session.add_all(strategy_list)
            self.session.commit()
        except Exception as e:
            LOG.logger.error('add_strategy: {}'.format(e))
            #print('add_strategy ERROR: ', e)
            return 0
        return 1
    
    def delete_strategy(self,strategy_name):
        try:
            del_sg = dbs.session.query(Strategy).filter_by(name=strategy_name).first()
            dbs.session.delete(del_sg)   
            dbs.session.commit()
        except Exception as e:
            #print('delete_strategy ERROR: ', e)
            LOG.logger.error('delete_strategy: {}'.format(e))
            return 0
        return 1
    
    def set_strategy_valid_status(self,strategy_name,valid=False):
        this_datetime = dt.datetime.now()
        try:
            self.session.query(Strategy).filter(Strategy.name==strategy_name).update({Strategy.is_valid:valid})
            self.session.query(Strategy).filter(Strategy.name==strategy_name).update({Strategy.lastupdate:this_datetime})
            self.session.commit()
        except Exception as e:
            #print('set_strategy_valid_status ERROR: ', e)
            LOG.logger.error('set_strategy_valid_status: {}'.format(e))
            return 0
        return 1
    
    def add_account(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        startdate = dt.datetime.now()
        account_list = []
        for data in datas:
            ac = Accountbase(uuid=data[0],type=data[1], username=data[2], password=data[3], email=data[4], startdate=data[5],initfund=data[6],trade_fee=data[7])
            account_list.append(ac)
        try:
            self.session.add_all(account_list)
            self.session.commit()
        except Exception as e:
            #print('add_account ERROR: ', e)
            LOG.logger.error('add_account: {}'.format(e))
            return 0
        return 1
    
    def delete_account(self,uuid):
        try:
            del_ac = dbs.session.query(Accountbase).filter_by(uuid=uuid).first()
            dbs.session.delete(del_ac)   
            dbs.session.commit()
        except Exception as e:
            LOG.logger.error('delete_account: {}'.format(e))
            return 0
        return 1
    
    def update_account(self,uuid,fund):
        #this_datetime = dt.datetime.now()
        try:
            self.session.query(Accountbase).filter(Accountbase.uuid==uuid).update({Accountbase.initfund:fund})
            #self.session.query(Accountbase).filter(Accountbase.name==uuid).update({Accountbase.initfund:this_datetime})
            self.session.commit()
        except Exception as e:
            LOG.logger.error('update_account: {}'.format(e))
            return 0
        return 1
    
    def add_accountrade(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        account_list = []
        for data in datas:
            print(data)
            ac = Accountrade(accid=data[0],max_position=data[1], max_hold=data[2], realfund=data[3], position=data[4],
                              primary_strategy=data[5],secondary_strategy=data[6],recordtime=data[7],is_valid=data[8])
            account_list.append(ac)
        try:
            self.session.add_all(account_list)
            self.session.commit()
        except Exception as e:
            LOG.logger.error('add_accountrade: {}'.format(e))
            return 0
        return 1
    
    def delete_accountrade(self,uuid):
        try:
            del_ac = dbs.session.query(Accountrade).filter_by(accid=uuid).first()
            dbs.session.delete(del_ac)   
            dbs.session.commit()
        except Exception as e:
            LOG.logger.error('delete_accountrade: {}'.format(e))
            return 0
        return 1
    
    def update_accountrade(self,uuid,position):
        #this_datetime = dt.datetime.now()
        try:
            self.session.query(Accountrade).filter(Accountrade.accid==uuid).update({Accountrade.position:position})
            #self.session.query(Accountbase).filter(Accountbase.name==uuid).update({Accountbase.initfund:this_datetime})
            self.session.commit()
        except Exception as e:
            LOG.logger.error('update_accountrade: {}'.format(e))
            return 0
        return 1
    
    def add_ordertype(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        account_list = []
        for data in datas:
            print(data)
            #<Ordertype(type='%s', reorder='%s', wait='%s',wave='%s')>
            ac = Ordertype(type=data[0],reorder=data[1], wait=data[2], wave=data[3])
            account_list.append(ac)
        try:
            self.session.add_all(account_list)
            self.session.commit()
        except Exception as e:
            LOG.logger.error('add_ordertype: {}'.format(e))
            return 0
        return 1
    
    def delete_ordertype(self,type):
        try:
            del_ac = dbs.session.query(Ordertype).filter_by(type=type).first()
            dbs.session.delete(del_ac)   
            dbs.session.commit()
        except Exception as e:
            LOG.logger.error('delete_ordertype: {}'.format(e))
            return 0
        return 1
    
    def update_ordertype(self,type,wait):
        #this_datetime = dt.datetime.now()
        try:
            self.session.query(Ordertype).filter(Ordertype.type==type).update({Ordertype.wait:wait})
            #self.session.query(Accountbase).filter(Accountbase.name==uuid).update({Accountbase.initfund:this_datetime})
            self.session.commit()
        except Exception as e:
            LOG.logger.error('update_ordertype: {}'.format(e))
            return 0
        return 1
    
    def add_order(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        account_list = []
        for data in datas:
            print(data)
            #Order(accid='%s', type='%s', direction='%s',code='%s',name='%s',price='%s',share='%s',status='%s',fee='%s',ordertime='%s')
            ac = Orders(accid=data[0],type=data[1], direction=data[2], code=data[3], name=data[4],
                              price=data[5],share=data[6],status=data[7],fee=data[8],ordertime=data[9])
            account_list.append(ac)
        try:
            self.session.add_all(account_list)
            self.session.commit()
        except Exception as e:
            LOG.logger.error('add_order: {}'.format(e))
            return 0
        return 1
    
    def delete_order(self,order_id):
        try:
            del_ac = dbs.session.query(Orders).filter_by(id=order_id).first()
            dbs.session.delete(del_ac)   
            dbs.session.commit()
        except Exception as e:
            LOG.logger.error('delete_order: {}'.format(e))
            return 0
        return 1
    
    def update_order_status(self,order_id,status):
        #this_datetime = dt.datetime.now()
        try:
            self.session.query(Orders).filter(Orders.id==order_id).update({Orders.status:status})
            #self.session.query(Accountbase).filter(Accountbase.name==uuid).update({Accountbase.initfund:this_datetime})
            self.session.commit()
        except Exception as e:
            LOG.logger.error('update_order_status: {}'.format(e))
            return 0
        return 1
    
    def add_potential(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        account_list = []
        for data in datas:
            print(data)
            #Potential(code='%s', name='%s', weight='%s', is_valid='%s', max_num='%s',addtime='%s')
            ac = Potential(code=data[0],name=data[1], weight=data[2], is_valid=data[3], 
                           max_num=data[4], addtime=data[5])
            account_list.append(ac)
        try:
            self.session.add_all(account_list)
            self.session.commit()
        except Exception as e:
            LOG.logger.error('add_potential: {}'.format(e))
            return 0
        return 1
    
    def delete_potential(self,code):
        try:
            del_ac = dbs.session.query(Potential).filter_by(code=code).first()
            dbs.session.delete(del_ac)   
            dbs.session.commit()
        except Exception as e:
            LOG.logger.error('delete_potential: {}'.format(e))
            return 0
        return 1
    
    def update_potential(self,code,is_valid):
        #this_datetime = dt.datetime.now()
        try:
            self.session.query(Potential).filter(Potential.code==code).update({Potential.is_valid:is_valid})
            #self.session.query(Accountbase).filter(Accountbase.name==uuid).update({Accountbase.initfund:this_datetime})
            self.session.commit()
        except Exception as e:
            LOG.logger.error('update_potential: {}'.format(e))
            return 0
        return 1


def initial_db_tables(dbs):
    #初始化表格 Strategy
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
    #初始化表格 Accountbase
    #Accountbase(uuid='%s',type='%s', username='%s', password='%s', email='%s', startdate='%s',initfund='%s',trade_fee='%s')
    account_datas = [('36007','A',None,None,'104450966@qq.com',startdate,120000,0.0023),
                     ('36008','A',None,None,'104450966@qq.com',startdate,100000,0.0023),]
    dbs.add_account(account_datas)
    dbs.update_account('36007', 100000)    
    dbs.delete_account(uuid='36008')
    #初始化表格 Accountrade
    #Accountrade(accid='%s', max_position='%s', max_hold='%s', realfund='%s', position='%s', primary_strategy='%s', secondary_strategy='%s', recordtime='%s',is_valid='%s')    
    accountrade_datas = [('36007',1,5,12000,0.8,1,None,startdate,True),
                         ('36008',1,5,11100,0.5,2,1,startdate,True)]
    
    dbs.add_accountrade(accountrade_datas)
    dbs.update_accountrade('36007', 0.3)    
    #dbs.delete_accountrade(uuid='36008')
    #初始化表格 Ordertype
    ordertype_datas = [('absolute',False,0,0),  #涨停价买，跌停价卖
                       ('now',True,0,0.005),  #现价买卖
                       ('delay',True,60,0.005),  #延时一定时间，现价买入
                       ('other',True,60,0)
                       ] 
    
    dbs.add_ordertype(ordertype_datas)
    dbs.update_ordertype('delay',120 )    
    #dbs.delete_ordertype(type='other')   
    #初始化表格 Order
    #Order(accid='%s', type='%s', direction='%s',code='%s',name='%s',price='%s',share='%s',status='%s',fee='%s',ordertime='%s')>
    order_datas = [('36007',1,'B','300017','顺网科技',16.5,500,'ordering',10,startdate),
                   ('36007',2,'S','300017','顺网科技',18.5,500,'ordering',10,startdate),
                   ('36008',1,'B','300053','同花顺',16.5,100,'ordering',10,startdate),
                   ('36008',1,'S','300053','东方财富',16.5,300,'ordering',10,startdate),
                   ]    
    dbs.add_order(order_datas)
    dbs.update_order_status(order_id=1, status='ordered')
    dbs.update_order_status(order_id=2, status='canceled')
    dbs.update_order_status(order_id=3, status='partial')
    dbs.delete_order(order_id=4)
    dbs.commit()
    #初始化表格 Potential
    #Potential(code='%s', name='%s', weight='%s', is_valid='%s', max_num='%s',addtime='%s')
    potential_datas = [('002412','新和成',10,True,300,startdate),
                       ('300012','同花顺',10,True,300,startdate),
                       ('600012','好莱客',10,True,300,startdate),
                       ('002212','分众传媒',10,True,300,startdate),
                       ]
    dbs.add_potential(potential_datas)
    dbs.update_potential('600012',False)
    dbs.delete_potential('300012')
    dbs.commit()
    dbs.close()
    
#initial_db_tables(dbs)
try:
    #initial_db(recreate=False)
    pass
except:
    pass

initial_db(recreate=True)
dbs = DBSession(echo=True)
initial_db_tables(dbs)
startdate = dt.datetime.now()
import sys
#sys.path.append("../logs")

#LOG.logger.info('分众传媒')
#initial_db_tables(dbs)