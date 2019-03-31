# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-03-31
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
apps = Flask(__name__)
db_path = os.path.dirname(os.path.abspath(__file__))  
db_path = db_path.replace('all','mocdel')
db_path = os.path.dirname(os.path.abspath(__file__))  
db_path = db_path.replace('appweb','trademodel')
apps.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path,'pytrader.db')
dbs = SQLAlchemy(apps)
#SQLALCHEMY_TRACK_MODIFICATIONS = True #C:\Python3.5\Lib\site-packages\flask_sqlalchemy
#SQLALCHEMY_COMMIT_TEARDOWN = True