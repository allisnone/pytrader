# -*- coding:utf-8 -*-
import json
CONFIG = {}
with open('config.json', 'r', encoding='utf-8') as f:
            CONFIG = json.loads(f.read())
            f.close()