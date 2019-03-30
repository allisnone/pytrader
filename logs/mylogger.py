# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-02-16
#https://www.cnblogs.com/yyds/p/6901864.html
import logging
import logging.handlers
import datetime
import base64
from .enc import aes_cbc_decrypt

class Logger(object):
    def __init__(self,logfile='all.log',errorfile='error.log',logname='mylogger',level=logging.DEBUG,tolist=['104450966@qq.com']):
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(level)
        rf_handler = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        f_handler = logging.FileHandler(errorfile)
        f_handler.setLevel(logging.ERROR)
        f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
        self.m_handler = None
        self.logger.addHandler(rf_handler)
        self.logger.addHandler(f_handler)
        #logger.addHandler(m_handler)
        self.tomails = tolist
        
    def set_tomails(self,tolist): 
        self.tomails = tolist
        return
    
    def set_mail_handle(self,subject,handle=None):
        rand = b'^\xe3\xb1*PxXR\xcb\x92\tc\xa2\x84\xf3W\xab\xca\xf9\x88\xb1)\x9b\xc7\xd4p\xb8\xf6b\xc7\xd7\x91'  #8Z
        gx = b'emd4MjAwMjIwMDJAMTYzLmNvbQ=='
        em = base64.decodestring(gx).decode('utf-8')
        if handle:
            self.m_handler = handle
        else:
            self.m_handler = logging.handlers.SMTPHandler(('smtp.163.com',25),
                                                 fromaddr= em,
                                                 toaddrs=self.tomails,
                                                 subject = subject,
                                                 credentials = (em,aes_cbc_decrypt(rand).decode('utf-8'))
                                                 )  
        
    def send_mail(self,subject = 'Just for logger test',handle=None):
        self.logger.info('Send mail message to {}'.format(self.tomails))
        self.set_mail_handle(subject,handle)
        self.logger.addHandler(self.m_handler)
        return
    
    def stop_send_mail(self):
        self.logger.removeHandler(self.m_handler)
        self.logger.info('Cancel send mail message to {}'.format(self.tomails))
        return
  
LOG = Logger(logfile='pytrader.log',errorfile='error.log',logname='mylogger',level=logging.DEBUG)
""" 
LOG = Logger(logfile='all.log',errorfile='error.log',logname='mylogger',level=logging.DEBUG)
LOG.logger.debug('debug message')
LOG.logger.info('info message')
LOG.logger.warning('warning message')
LOG.send_mail(subject='add error message mail')
LOG.logger.error('error message')
LOG.stop_send_mail()
LOG.logger.critical('critical message')
LOG.logger.critical('critical message1')
"""