# -*- coding:utf-8 -*-
import os
import json
import csv
import configparser
import sys
#sys.path.append('..')
#import mail.sendEmail as sm
class MyFile:
    # mainly use to read json, csv, ini, txt file
    def __init__(self,file_name='abc.txt',initial_data=True,encoding='utf-8'):
        self.file = file_name
        self.type = file_name.split('.')[-1]
        self.encoding = encoding
        self.datas = None
        if initial_data:
           self.read_file()
    
    def set_type(self,type):
        self.type = type
        return
    
    def read_file(self):
        if self.type == 'txt':
            self.datas = self.read_txt()
        elif self.type == 'json':
            self.datas = self.read_json()
        elif self.type == 'ini':
            self.datas = self.read_ini()
        elif self.type == 'csv':
            self.datas = self.read_csv()
        else:
            print('Unsupport file type!!!')
        return
    
    def read_txt(self):
        with open(self.file, 'r', encoding=self.encoding) as f:
            lines = f.readlines()
            f.close()
        return lines
    
    def write_txt(self,mylist):
        """
        :parama mylist, list type
        """
        #myList=[[1,2,3],[4,5,6]]
        with open(self.file, 'w', encoding=self.encoding) as f:
            f.writelines(mylist)
            f.close()
        return
    
    def read_json(self):
        with open(self.file, 'r', encoding=self.encoding) as f:
            j = json.loads(f.read())
            f.close()
        return j
    
    def write_json(self,d,indent=4):
        """
        :parama d, dict type
        """
        with open(self.file, 'w', encoding=self.encoding) as f:
            f.write(json.dumps(d, indent))
            f.close()
        return
    
    def read_ini(self):
        #with open(self.file)as f :#, 'w', encoding=self.encoding) as f:
        try:
            config = configparser.ConfigParser()
            config.read(self.file)#, encoding=self.encoding)
            #config.readfp(f)
            #s = config.sections()
            #o = config.options("mysql")
            #i = config.items("mysql")
            #g = config.get("mysql","db_host")
            #config.add_section("book")
            #config.set("book", "title", "the python standard library")
            #config.write(open('1.ini', "w"))
            #f.close()
            return config
        except Exception as e:
            print(e)
            return None
    
    def read_csv(self):
        with open(self.file,'rb',encoding=self.encoding) as f:  
            r = csv.reader(f)
            f.close()
        return r
    
    def write_csv(self,mylist):
        """
        :parama mylist, list type
        """
        #myList=[[1,2,3],[4,5,6]]
        with open(self.file,'wb',encoding=self.encoding) as f:      
            myWriter=csv.writer(f)  
            #myWriter.writerow([7,8,9])     
            myWriter.writerows(mylist)
            f.close()
        return