# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-03-31
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
db_path = os.path.dirname(os.path.abspath(__file__))  
db_path = db_path.replace('all','mocdel')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://pytrader.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)