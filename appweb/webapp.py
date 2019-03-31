# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-03-31
# flask_sqlalchemy.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from trademodel.appmodels import *
from appweb.appflask import apps   
@apps.route('/strategy')
def strategies():
    users = Strategy.query.all()
    return "<br>".join(["{0}: {1}".format(user.name, user.comments) for user in users])
# 查询
@apps.route('/strategy/<int:strategy_id>')
def strategy(strategy_id):
    user = Strategy.query.filter_by(id=strategy_id).one()
    return "{0}: {1}".format(user.name, user.comments)
# 运行
if __name__ == '__main__':
    apps.run('127.0.0.1', 5000)