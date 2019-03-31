# -*- coding:utf-8 -*-
import json,os
from comm.logger import Logger
import logging
CONFIG = {}
HOME_PATH = os.path.dirname(os.path.abspath(__file__)).replace('config','')
config_file = os.path.join(HOME_PATH,'config','config.json')
with open(config_file, 'r', encoding='utf-8') as f:
            CONFIG = json.loads(f.read())
            f.close()
            
LOG_PATH = os.path.join(HOME_PATH,'logs')
DB_PATH = os.path.join(HOME_PATH,'trademodel','pytrader.db')
LOG = Logger(logfile=os.path.join(LOG_PATH,'pytrader.log'),errorfile=os.path.join(LOG_PATH,'error.log'),logname='mylogger',level=logging.DEBUG)
