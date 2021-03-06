# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-03-31
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from trademodel.appmodels import *
from trademodel.appmodels import Strategy,Accountbase,Accountrade,Ordertype,Orders,Potential,Deal,Capital,dt,create_engine
from appweb.appflask import apps
@apps.route('/strategy')
def strategies():
    users = Strategy.query.all()
    return "<br>".join(["{0}: {1}".format(user.name, user.comments) for user in users])

# 查询
@apps.route('/strategy/<int:strategy_id>')
def strategy1(strategy_id):
    user = Strategy.query.filter_by(id=strategy_id).one()
    return "{0}: {1}".format(user.name, user.comments)
# 运行
if __name__ == '__main__':
    apps.run('127.0.0.1', 5000)