#!/usr/bin/python
# -*- coding:utf-8 -*-
"""

"""
import os
import time
import datetime
import sys
import signal
reload(sys)
sys.setdefaultencoding('utf8')
from Connalert import *
from apscheduler.schedulers.background import BackgroundScheduler

def gotodo():
    try :
        c = Connalert('a.out','http://xx:8080/getallconnect','xx','xx','localhost',3306,'root','')
        c.getjson()
        c.domysql()
        c.doprint()
    except Exception,e:
        print e
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(gotodo, 'interval', minutes=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown() 
