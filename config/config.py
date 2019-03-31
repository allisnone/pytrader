# -*- coding:utf-8 -*-
import json,os
CONFIG = {}
with open('config.json', 'r', encoding='utf-8') as f:
            CONFIG = json.loads(f.read())
            f.close()
            

HOME_PATH = os.path.dirname(os.path.abspath(__file__)).replace('config','')
