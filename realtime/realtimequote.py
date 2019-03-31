# -*- coding: utf-8 -*-
'''
Created on 2016-8-1
@author: Jason
'''
import urllib.request
import csv
import pandas as pd
import datetime as dt
import numpy as np
from config.config import LOG
#http://hq.sinajs.cn/list=sh000001

class QQuotation:
    def __init__(self,code,baseurl='http://qt.gtimg.cn/q=',interval=30,decode='gbk'):
        self.code = code
        self.interval = 20
        self.decode = decode
        self.base_url = baseurl
        self.symbol = self.format_symbol()
        
    def set_base_url(self,url):
        self.base_url = url    
        
    def format_symbol(self):
        """
        转化为qq识别的代码
        """
        symbol = 'sz{}'.format(self.code)
        index_symbol_maps = {'sh':'000001','sz':'399001','zxb':'399005','cyb':'399006',
                             'sh50':'000016','sz300':'399007','zx300':'399008','hs300':'000300'}
        if self.code in list(index_symbol_maps.keys()): #index
            symbol = 'sz%s' % index_symbol_maps[self.code]
            if index_symbol_maps[self.code]<'100000':
                symbol = symbol.replace('sz', 'sh')
        elif self.code>='500000':  #stock or fund
            symbol = symbol.replace('sz', 'sh')
        else:
            pass
        return symbol
    
    def get_url_content(self,url=''):  #qq: decode_type='gbk'
        """
        请求qq接口的内容
        """
        if url:
            pass
        else:
            url = self.base_url + self.symbol
        #print('url=',url)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        #the_page = response.read() 
        content = response.read().decode(self.decode)#('utf-8')#.encode('utf-8') 
        return content
    
    def get_quote_data(self,url=''):  #qq: decode_type='gbk'
        """
        请求qq接口的内容
        """
        """
        v_sz000858="51~五 粮 液~000858~
        34.46~34.42~34.25~355547~177888~177660~34.46~588~34.45~4428~34.44~124~34.43~197~34.42~161
        ~34.47~1016~34.48~196~34.49~77~34.50~890~34.51~720~
        15:00:01/34.46/2428/S/8368163/12416|14:57:00/34.45/61/S/210152/12316|14:56:57/34.45/51/S/175736/12314|
        14:56:54/34.46/38/B/130946/12312|14:56:48/34.45/23/S/79245/12310|14:56:48/34.46/10/B/34460/12308
        ~20160808150134~0.04~0.12~34.52~33.53~34.45/353119/1202383921~355547~121075~
        0.94~19.02~~34.52~33.53~2.88~1307.99~1308.09~2.83~37.86~30.98~";
        0: 未知  
        1: 名字  
        2: 代码  
        3: 当前价格  
        4: 昨收  
        5: 今开  
        6: 成交量（手）  
        7: 外盘  
        8: 内盘  
        9: 买一  
        10: 买一量（手）  
        11-18: 买二 买五  
        19: 卖一  
        20: 卖一量  
        21-28: 卖二 卖五  
        29: 最近逐笔成交  
        30: 时间  
        31: 涨跌  
        32: 涨跌%  
        33: 最高  
        34: 最低  
        35: 价格/成交量（手）/成交额  
        36: 成交量（手）  
        37: 成交额（万）  
        38: 换手率  
        39: 市盈率  
        40:   
        41: 最高  
        42: 最低  
        43: 振幅  
        44: 流通市值  
        45: 总市值  
        46: 市净率  
        47: 涨停价  
        48: 跌停价  
        """
        url = self.base_url + self.symbol
        LOG.logger.info('qq quote url: {}'.format(url))
        content =''
        try: 
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            #the_page = response.read() 
            content = response.read().decode(self.decode)#('utf-8')#.encode('utf-8') 
            if len(content.split('"'))==1:
                return list()
        except Exception as e:
            LOG.logger.error('qq quote url: {0}, {1}'.format(url,e))
            return list()
        data = content.split('"')[1].split('~')
        return data
    
    def get_quote_data_dict(self,q_data=[],url=''):
        data_dict = dict()
        if q_data:
            pass
        else:
            q_data =self.get_quote_data(url)
        if len(q_data)>=48:
            data_dict={
                    'name': q_data[1],
                    'code': self.code,
                    'now': float(q_data[3]),
                    'close': float(q_data[3]),
                    'close0': float(q_data[4]),
                    'open': float(q_data[5]),
                    'volume': float(q_data[6]) * 100,
                    'bid_volume': int(q_data[7]) * 100,
                    'ask_volume': float(q_data[8]) * 100,
                    'bid1': float(q_data[9]),
                    'bid1_volume': int(q_data[10]) * 100,
                    'bid2': float(q_data[11]),
                    'bid2_volume': int(q_data[12]) * 100,
                    'bid3': float(q_data[13]),
                    'bid3_volume': int(q_data[14]) * 100,
                    'bid4': float(q_data[15]),
                    'bid4_volume': int(q_data[16]) * 100,
                    'bid5': float(q_data[17]),
                    'bid5_volume': int(q_data[18]) * 100,
                    'ask1': float(q_data[19]),
                    'ask1_volume': int(q_data[20]) * 100,
                    'ask2': float(q_data[21]),
                    'ask2_volume': int(q_data[22]) * 100,
                    'ask3': float(q_data[23]),
                    'ask3_volume': int(q_data[24]) * 100,
                    'ask4': float(q_data[25]),
                    'ask4_volume': int(q_data[26]) * 100,
                    'ask5': float(q_data[27]),
                    'ask5_volume': int(q_data[28]) * 100,
                    'recent_trade': q_data[29],  # 换成英文  # 最近逐笔成交
                    'quot_time':dt.datetime.now(),
                    'datetime': dt.datetime.strptime(q_data[30], '%Y%m%d%H%M%S'),
                    'date': dt.datetime.strptime(q_data[30], '%Y%m%d%H%M%S').strftime('%Y/%m/%d'),
                    'increase': float(q_data[31]),  # 换成英文 #涨跌
                    'increase_rate': float(q_data[32]),  # 换成英文  #涨跌(%)
                    'high': float(q_data[33]),
                    'low': float(q_data[34]),
                    'price_volume_amount': q_data[35],  # 换成英文  价格/成交量(手)/成交额
                    'volume': int(q_data[36]) * 100,  # 换成英文
                    'amount': float(q_data[37]) * 10000,  # 换成英文  #成交额(万)
                    'turnover': float(q_data[38]) if q_data[38] != '' else None,
                    'PE': float(q_data[39]) if q_data[39] != '' else None,
                    'unknown': q_data[40],
                    'high_2': float(q_data[41]),  # 意义不明
                    'low_2': float(q_data[42]),  # 意义不明
                    'wave': float(q_data[43]),  # 换成英文  振幅
                    'circulation': float(q_data[44]) if q_data[44] != '' else None,  # 换成英文  流通市值
                    'total_market': float(q_data[45]) if q_data[44] != '' else None,  # 换成英文, 总市值
                    'PB': float(q_data[46]),
                    'topest': float(q_data[47]),  # 换成英文  涨停价
                    'lowest': float(q_data[48])  # 换成英文     跌停价
                    }
        else:
            pass
        return data_dict
    
    
    def get_zijin(self):
        #http://qt.gtimg.cn/q=ff_sz000858
        """
        v_ff_sz000858="sz000858~72203.00~78804.40~-6601.40~-5.45~48872.20~42271.00~6601.20~5.45~121075.20~238259.6~257086.6~五 粮 液
        ~20160808~20160805^35557.70^43932.20~20160804^30988.10^33894.30~20160803^45746.90^40036.00~20160802^53763.90^60419.70";
        
        0: 代码  
        1: 主力流入  
        2: 主力流出  
        3: 主力净流入  
        4: 主力净流入/资金流入流出总和  
        5: 散户流入  
        6: 散户流出  
        7: 散户净流入  
        8: 散户净流入/资金流入流出总和  
        9: 资金流入流出总和1+2+5+6  
        10: 未知  
        11: 未知  
        12: 名字  
        13: 日期  
        """
        self.set_base_url(url='http://qt.gtimg.cn/q=ff_')
        return self.get_quote_data()
    
    def get_pankou(self):
        """
        http://qt.gtimg.cn/q=s_pksz000858  
    
        0: 买盘大单  
        1: 买盘小单  
        2: 卖盘大单  
        3: 卖盘小单 
        """
        self.set_base_url(url='http://qt.gtimg.cn/q=s_pk')
        return self.get_quote_data()
    
    def get_zhaiyao(self):
        """
        http://qt.gtimg.cn/q=s_sz000858
            
        0: 未知  
        1: 名字  
        2: 代码  
        3: 当前价格  
        4: 涨跌  
        5: 涨跌%  
        6: 成交量（手）  
        7: 成交额（万）  
        8:   
        9: 总市值  
        """
        self.set_base_url(url='http://qt.gtimg.cn/q=s_')
        #url = 'http://qt.gtimg.cn/q=s_{}'.format(self.symbol)
        return self.get_quote_data()
    
q = QQuotation(code='300017')
data = q.get_quote_data_dict()
print(data)
z = q.get_zijin()
print(z)
print(q.get_pankou())
print(q.get_zhaiyao())
