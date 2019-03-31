# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-03-31
# flask_sqlalchemy.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from trademodel.appmodels import *
from appflask import db,app
"""
app = Flask(__name__)
db_path = os.path.dirname(os.path.abspath(__file__))  
db_path = db_path.replace('appweb','trademodel')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path,'pytrader.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
"""
# 定义ORM
""""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    def __init__(self, name, email):
        self.name = name
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.name
    # 创建表格、插入数据
@app.before_first_request
def create_db():
  # Recreate database each time for demo
  #db.drop_all()
  db.create_all()
  admin = User('admin', 'admin@example.com')
  db.session.add(admin)
  guestes = [User('guest1', 'guest1@example.com'),
        User('guest2', 'guest2@example.com'),
        User('guest3', 'guest3@example.com'),
        User('guest4', 'guest4@example.com')]
  db.session.add_all(guestes)
  db.session.commit()
# 查询


class Strategy(db.Model):
    __tablename__ = 'strategy'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True)
    startdate = db.Column(db.DateTime)
    lastupdate = db.Column(db.DateTime)#,onupdate=func.now)
    is_valid = db.Column(db.Boolean,default=True)
    comments = db.Column(db.Text)
    
    
    accountrade = relationship("Accountrade", back_populates='strategy')
    def __repr__(self):
        return "<Strategy(name='%s', startdate='%s', lastupdate='%s', is_valid='%s', comments='%s')>" % (
                            self.name, self.startdate,self.lastupdate, self.is_valid,self.comments)
"""    
@app.route('/strategy')
def users():
  users = Strategy.query.all()
  return "<br>".join(["{0}: {1}".format(user.name, user.comments) for user in users])
# 查询
@app.route('/strategy/<int:id>')
def user(id):
  user = Strategy.query.filter_by(id=id).one()
  return "{0}: {1}".format(user.name, user.comments)
# 运行
if __name__ == '__main__':
  app.run('127.0.0.1', 5000)