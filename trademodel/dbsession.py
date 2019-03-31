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
"""
from sqlalchemy import *#Column, String, create_engine,relationship
from sqlalchemy.orm import sessionmaker,relationship,aliased
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt
from comm.logger import LOG
"""
#from sqlalchemy import *#Column, String, create_engine,relationship
from sqlalchemy.orm import sessionmaker
#from config import HOME_PATH
from trademodel.appmodels import Strategy,Accountbase,Accountrade,Ordertype,Orders,Potential,Deal,Capital,dt,create_engine
from comm.logger import LOG
#from trademodel.model import Base
import os
#from appmodel import *
# 创建对象的基类:
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class DBSession:
    def __init__(self,db='pytrader.db',echo=False):
        db_path = os.path.dirname(os.path.abspath(__file__))  
        #db_path = db_path.replace('trademodel','appweb')
        db = os.path.join(db_path,db)
        self.engine = create_engine('sqlite:///' + db + '?check_same_thread=False', echo=echo)
        # 创建DBSession类型:
        Session = sessionmaker(bind=self.engine)
        # DBSession对象可视为当前数据库连接
        # 创建session对象:
        self.session = Session()
    
    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            LOG.logger.error('Fail to commit and rollback: {}'.format(e))
        return
    
    def close(self):
        self.session.close()
        return

    def add_strategy(self,datas=[]):
        #add strategy
        #插入
        #startdate = dt.datetime.strptime('2019-3-24','%Y-%m-%d')
        #startdate = dt.datetime.now()
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
            del_sg = self.session.query(Strategy).filter_by(name=strategy_name).first()
            self.session.delete(del_sg)   
            self.session.commit()
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
        #startdate = dt.datetime.now()
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
            del_ac = self.session.query(Accountbase).filter_by(uuid=uuid).first()
            self.session.delete(del_ac)   
            self.session.commit()
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
            del_ac = self.session.query(Accountrade).filter_by(accid=uuid).first()
            self.session.delete(del_ac)   
            self.session.commit()
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
            del_ac = self.session.query(Ordertype).filter_by(type=type).first()
            self.session.delete(del_ac)   
            self.session.commit()
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
            del_ac = self.session.query(Orders).filter_by(id=order_id).first()
            self.session.delete(del_ac)   
            self.session.commit()
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
            del_ac = self.session.query(Potential).filter_by(code=code).first()
            self.session.delete(del_ac)   
            self.session.commit()
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
    dbs.commit()
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
"""    
#initial_db_tables(dbs)
try:
    #initial_db(recreate=False)
    pass
except:
    pass

initial_db(recreate=True)
dbs = DBSession(echo=True)
initial_db_tables(dbs)
"""
#startdate = dt.datetime.now()
#import sys
#sys.path.append("../logs")
#LOG.logger.info('分众传媒')
#initial_db_tables(dbs)