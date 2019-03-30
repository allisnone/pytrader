# -*- coding:utf-8 -*-
from comm import fileOperation
from logs.mylogger import LOG

f = fileOperation.MyFile('./config/config.json')
print(f.datas)