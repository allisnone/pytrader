# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-02-16
#https://docs.python.org/3/library/sqlite3.html
#https://www.sqlite.org/index.html
import sqlite3
import os

class Mysqlite():
    def __init__(self,db_path='',memory=False):
        self.connect = None
        self.cursor = None
        self.create_sqlite(db_path,memory)
        
    def create_sqlite(self, path='',memory=False):
        conn = None
        if not memory:
            self.connect =  sqlite3.connect(path)
        else:
            self.connect = sqlite3.connect(':memory:')
        self.cursor = self.connect.cursor()
        
    def close(self):
        self.cursor.close()
        self.connect.close()
    
    def _join_str(self,fields, default='',specify=','):
        """
        把list或者tuple转化为str, 以逗号或者其他特殊字符连接
        """
        re = default
        if fields:
            if isinstance(fields,str):
                re = fields
            elif isinstance(fields, list) or isinstance(fields, tuple):
                re = specify.join(fields)
            else:
                pass
        return re
    
    def create_table(self,table,columns=[]):
        """
        创建table：
        table: str, table name
        columns: table 列的列表或者tuple，保护sql的数据类型
        """
        #con.execute("create table person (id integer primary key, firstname varchar unique)")
        #cursor.execute(sql,{'st_name':name, 'st_username':username, 'id_num':id_num})
        #columns = ('id integer primary key', 'firstname varchar unique')
        sql = "create table %s (%s);" % (table,self._join_str(columns))
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            print('create_table Exception: ',e)
        return  
    
    def get_table(self,table, fields='',where={'firsname':'b'}):  
        """
        获取table的所有数据
        table: str
        fields: select 的列
        where: 过滤条件，只支持=
        """
        sql = "select %s from %s" % (self._join_str(fields,'*'),table)
        a = ';'
        if where:
            a = ' where '+ ' '.join(['%s="%s"'%(k,v) for k,v in where.items()]) + ';'
        try: 
            print('sql=',sql+a)
            results = self.cursor.execute(sql+a)# 遍历打印输出
            datas = results.fetchall()
            return datas
        except Exception as e:
            print('get_table Exception: ',e)
        #self.cursor.close()
        return  []
    
    def drop_table(self,table):
        sql = 'DROP TABLE IF EXISTS ' + table
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            return 1
        except Exception as e:
            print('drop_table Exception: ',e)
        return 0
    
    def insert(self,table,datas):
        """
        table: str, table name
        datas: list, each element will be tuple type
        """
        if isinstance(datas,list) or isinstance(datas,tuple):
            pass
        else:
            return 
        col_count = len(datas[0])
        col_str = ','.join(['?']*col_count)
        sql = 'INSERT INTO %s VALUES (%s)' % (table, col_str)
        try:
            self.cursor.executemany(sql,datas)
            self.connect.commit()
            return 1
        except Exception as e:
            print('insert Exception: ',e)
        #cursor.execute(sql,{'st_name':name, 'st_username':username, 'id_num':id_num})
        return 0
    
    def update(self,table,field,where=[], datas=[]):
        """
        更新特定字段
        table: str
        field: 更新的域
        where: 过滤条件
        datas: 更新的值和条件值组成的tuple， (更新的值,条件值1,条件值2,...)，条件是与关系 
        """
        where_str = self._join_str(where, default='',specify='=? ') + '=?;'
        update_sql = 'UPDATE %s SET %s=? ' % (table,field) + ' where ' +  where_str
        #print('update_sql=',update_sql)
        try:
            self.cursor.executemany(update_sql,datas)
            self.connect.commit()
            return 1
        except Exception as e:
            print('update Exception: ',e)
        return 0
    
    def delete(self,table,where=[], datas=[]):
        """
        删除某行
        table: str
        where: 过滤条件，列名称组成的列表；where为空时，删除全部行
        datas: 条件值组成的tuple， (条件值1,条件值2,...)，与关系
        """
        #delete_sql = 'DELETE FROM student WHERE NAME = ? AND ID = ? '
        where_str = self._join_str(where, default='',specify='=? ') + '=?;'
        delete_sql = 'DELETE FROM %s' % table + ' where ' +  where_str
        try:
            if not where:
                self.cursor.executemany(delete_sql,datas)
            else:
                self.cursor.executemany('DELETE FROM %s' % table)
            self.connect.commit()
            return 1
        except Exception as e:
            print('delete Exception: ',e)
        return 0
    
    def execute_script(self,sql):
        """
        create table person(
            firstname,
            lastname,
            age
        );
    
        create table book(
            title,
            author,
            published
        );
        CREATE TABLE `student`(
            `id` int(11) NOT NULL,
            `name` varchar(20) NOT NULL,
            `gender` varchar(4) DEFAULT NULL,
            `age` int(11) DEFAULT NULL,
            `address` varchar(200) DEFAULT NULL,
            `phone` varchar(20) DEFAULT NULL,
            PRIMARY KEY (`id`)
        );
        insert into book(title, author, published)
        values (
            'Dirk Gently''s Holistic Detective Agency',
            'Douglas Adams',
            1987
        );
        """
        try:
            self.cursor.executescript(sql)
            self.connect.commit()
            return 1
        except Exception as e:
            print('execute_script Exception: ',e)
        return 0
    
    def backup(self,new='backup.db'):
        #sqlite3 >=3.7
        def progress(status, remaining, total):
            print('Copied {total-remaining} of {total} pages...')
            return
        with sqlite3.connect(new) as bck:
            self.connect.backup(bck, pages=1, progress=progress)
        return
    
if __name__ == '__main__':
    sql3 = Mysqlite(db_path='test.db',memory=False)
    columns = ('id integer primary key', 'firstname varchar unique')
    sql3.create_table('table1', columns)
    datas1 = [(1,'a'),(2,'b'),(3,'c')]
    datas2 = [(1,'e'),(2,'f'),(3,'g')]
    sql3.insert('table1', datas1)
    table1_data = sql3.get_table(table='table1', fields='', where={'firstname':'b'})
    print('table1_data=',table1_data)
    sql3.insert('person', datas2)
    table2_data = sql3.get_table(table='person', fields='', where='')
    print('table2_data=',table2_data)
    sql3.update(table='table2',field='firstname',where=['id'], datas=[('h',2)])
    table2_data1 = sql3.get_table(table='table2', fields='', where='')
    print('table2_data1=',table2_data1)
    #sql3.drop_table('table1')
    #sql3.backup('new.db')
    sql3.close()